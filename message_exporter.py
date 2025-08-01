#!/usr/bin/env python3
"""
Message Exporter - Streamlined tool to export complete message history

Copyright (c) 2025 Ronnit Peter. All rights reserved.
This software is available under a dual-license approach:
- Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0) for personal/academic use
- Commercial license available for commercial use
See LICENSE file for full terms.
"""

import os
import sqlite3
import json
import re
import sys
from datetime import datetime

def find_contact_by_name_or_number(search_term):
    """
    Find contact by name or phone number
    """
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    
    if not os.path.exists(db_path):
        print("❌ Messages database not found!")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Try different search patterns
        search_patterns = [
            search_term,  # Exact match
            f"%{search_term}%",  # Contains
            f"+1{search_term.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')}",  # US format
            f"+{search_term.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')}",  # International format
        ]
        
        for pattern in search_patterns:
            cursor.execute("SELECT id FROM handle WHERE id LIKE ?", (pattern,))
            result = cursor.fetchone()
            if result:
                conn.close()
                return result[0]
        
        conn.close()
        return None
        
    except Exception as e:
        print(f"❌ Error searching for contact: {e}")
        return None

def extract_complete_text(attributed_body_str):
    """
    Extract complete text from attributedBody string
    """
    if not attributed_body_str:
        return None
    
    # Look for complete text patterns
    patterns = [
        r'NSString.*?([A-Za-z0-9\s\.,!?@#$%^&*()_+\-=\[\]{}|;:"\'<>?/~`]{8,})',
        r'([A-Za-z0-9\s\.,!?@#$%^&*()_+\-=\[\]{}|;:"\'<>?/~`]{10,})',
        r'([A-Za-z]{4,}\s+[A-Za-z\s]{4,})',  # Words with spaces
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, attributed_body_str)
        if matches:
            for match in matches:
                # Filter out binary data
                if (len(match) > 7 and 
                    not all(ord(c) < 32 for c in match) and
                    not match.startswith('NS') and
                    not match.startswith('class') and
                    not match.startswith('$') and
                    not match.startswith('null') and
                    not 'streamtyped' in match.lower() and
                    not 'utableData' in match):
                    return match.strip()
    
    return None

def clean_extracted_text(text):
    """
    Clean up extracted text by removing artifacts
    """
    if not text:
        return None
    
    # Remove common artifacts
    cleaned = text
    
    # Remove binary prefixes
    cleaned = re.sub(r'^x[0-9a-f]+[+#]', '', cleaned)
    cleaned = re.sub(r'^x[0-9a-f]+', '', cleaned)
    
    # Remove single characters that are artifacts
    if len(cleaned) <= 2 and cleaned.isalpha():
        return None
    
    # Remove binary data patterns
    cleaned = re.sub(r"'\(\)\*Z\$classnameX\$classes[^']*", "", cleaned)
    cleaned = re.sub(r"'-\./4:>\?[^']*", "", cleaned)
    cleaned = re.sub(r"streamtyped", "", cleaned)
    cleaned = re.sub(r"utableData", "", cleaned)
    
    # Clean up whitespace
    cleaned = cleaned.strip()
    
    # Skip if too short after cleaning
    if len(cleaned) < 3:
        return None
    
    return cleaned

def export_messages(contact_id, contact_name):
    """
    Export complete message history for a contact
    """
    print(f"📨 Exporting messages for: {contact_name} ({contact_id})")
    print("=" * 60)
    
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all messages for this contact
        cursor.execute("""
            SELECT 
                message.ROWID,
                message.text,
                message.date,
                message.is_from_me,
                message.cache_has_attachments,
                message.attributedBody,
                message.service,
                datetime(message.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as readable_date
            FROM message 
            JOIN handle ON message.handle_id = handle.ROWID
            WHERE handle.id = ?
            ORDER BY message.date DESC
        """, (contact_id,))
        
        messages = cursor.fetchall()
        print(f"✅ Found {len(messages)} messages")
        
        if not messages:
            print("❌ No messages found for this contact")
            return False
        
        # Process and clean messages
        clean_messages = []
        
        for msg in messages:
            rowid = msg[0]
            text = msg[1]
            date = msg[2]
            is_from_me = msg[3]
            has_attachments = msg[4]
            attributed_body = msg[5]
            service = msg[6]
            readable_date = msg[7]
            
            # Try to get complete text
            complete_text = None
            
            # First try the text field
            if text and text.strip():
                complete_text = text
            else:
                # Try to extract from attributedBody
                if attributed_body:
                    body_str = str(attributed_body)
                    complete_text = extract_complete_text(body_str)
            
            # Clean the extracted text
            if complete_text:
                cleaned_text = clean_extracted_text(complete_text)
                if cleaned_text:
                    # Create clean message object
                    clean_msg = {
                        'rowid': rowid,
                        'date': date,
                        'is_from_me': bool(is_from_me),
                        'readable_date': readable_date,
                        'text': cleaned_text,
                        'service': service,
                        'has_attachments': bool(has_attachments)
                    }
                    clean_messages.append(clean_msg)
        
        # Sort by date (oldest first)
        clean_messages.sort(key=lambda x: x['date'])
        
        print(f"✅ Cleaned {len(clean_messages)} messages")
        
        # Create output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', contact_name)
        
        # Create simple conversation
        create_simple_conversation(clean_messages, contact_name, contact_id, timestamp, safe_name)
        
        # Create detailed conversation
        create_detailed_conversation(clean_messages, contact_name, contact_id, timestamp, safe_name)
        
        # Create summary
        create_summary(clean_messages, contact_name, contact_id, timestamp, safe_name)
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error exporting messages: {e}")
        return False

def create_simple_conversation(messages, contact_name, contact_id, timestamp, safe_name):
    """
    Create simple conversation format
    """
    output_file = f"conversation_{safe_name}_{timestamp}.txt"
    
    lines = []
    lines.append("💬 MESSAGE CONVERSATION")
    lines.append("=" * 60)
    lines.append(f"📱 Contact: {contact_name} ({contact_id})")
    lines.append(f"📅 Date Range: {messages[0]['readable_date']} to {messages[-1]['readable_date']}")
    lines.append(f"📊 Total Messages: {len(messages)}")
    lines.append("")
    
    for i, msg in enumerate(messages, 1):
        sender = "You" if msg['is_from_me'] else contact_name
        timestamp = msg['readable_date']
        text = msg['text']
        
        lines.append(f"{i:3d}. [{timestamp}] {sender}: {text}")
        lines.append("")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Simple conversation saved to: {output_file}")

def create_detailed_conversation(messages, contact_name, contact_id, timestamp, safe_name):
    """
    Create detailed conversation format
    """
    output_file = f"detailed_conversation_{safe_name}_{timestamp}.txt"
    
    lines = []
    lines.append("💬 DETAILED MESSAGE CONVERSATION")
    lines.append("=" * 60)
    lines.append(f"📱 Contact: {contact_name} ({contact_id})")
    lines.append(f"📅 Date Range: {messages[0]['readable_date']} to {messages[-1]['readable_date']}")
    lines.append(f"📊 Total Messages: {len(messages)}")
    lines.append("")
    lines.append("📋 CONVERSATION:")
    lines.append("-" * 60)
    lines.append("")
    
    for i, msg in enumerate(messages, 1):
        sender = "You" if msg['is_from_me'] else contact_name
        receiver = contact_name if msg['is_from_me'] else "You"
        timestamp = msg['readable_date']
        text = msg['text']
        
        lines.append(f"{i:3d}. [{timestamp}]")
        lines.append(f"    FROM: {sender}")
        lines.append(f"    TO: {receiver}")
        lines.append(f"    MESSAGE: {text}")
        
        if msg.get('service'):
            lines.append(f"    📱 Service: {msg['service']}")
        
        lines.append("")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Detailed conversation saved to: {output_file}")

def create_summary(messages, contact_name, contact_id, timestamp, safe_name):
    """
    Create conversation summary
    """
    output_file = f"summary_{safe_name}_{timestamp}.txt"
    
    lines = []
    lines.append("📋 CONVERSATION SUMMARY")
    lines.append("=" * 60)
    lines.append(f"📱 Contact: {contact_name} ({contact_id})")
    lines.append("")
    
    # Count messages by sender
    you_messages = [msg for msg in messages if msg['is_from_me']]
    contact_messages = [msg for msg in messages if not msg['is_from_me']]
    
    lines.append(f"📊 Message Count:")
    lines.append(f"  You: {len(you_messages)} messages")
    lines.append(f"  {contact_name}: {len(contact_messages)} messages")
    lines.append(f"  Total: {len(messages)} messages")
    lines.append("")
    
    # Show all messages
    lines.append("📝 All Messages:")
    lines.append("-" * 30)
    
    for i, msg in enumerate(messages, 1):
        sender = "You" if msg['is_from_me'] else contact_name
        text = msg['text']
        timestamp = msg['readable_date']
        lines.append(f"{i:2d}. [{timestamp}] {sender}: {text}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Summary saved to: {output_file}")

def main():
    """
    Main function
    """
    print("🎯 Message Exporter")
    print("=" * 60)
    print("Export complete message history for any contact")
    print("")
    
    if len(sys.argv) != 2:
        print("Usage: python3 message_exporter.py <phone_number_or_name>")
        print("")
        print("Examples:")
        print("  python3 message_exporter.py +12363381146")
        print("  python3 message_exporter.py \"John Doe\"")
        print("  python3 message_exporter.py 2363381146")
        return
    
    search_term = sys.argv[1]
    print(f"🔍 Searching for: {search_term}")
    
    # Find the contact
    contact_id = find_contact_by_name_or_number(search_term)
    
    if not contact_id:
        print("❌ Contact not found!")
        print("")
        print("💡 Tips:")
        print("  - Try the exact phone number format")
        print("  - Try the contact name as it appears in Messages")
        print("  - Try different formats (with/without +1, with/without dashes)")
        return
    
    print(f"✅ Found contact: {contact_id}")
    
    # Export messages
    success = export_messages(contact_id, contact_id)
    
    if success:
        print("")
        print("🎉 Export completed successfully!")
        print("📁 Check the generated files for your conversation history.")
    else:
        print("")
        print("❌ Export failed!")

if __name__ == '__main__':
    main() 