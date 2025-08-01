#!/usr/bin/env python3
"""
Conversation Batcher - Split large conversation files into manageable chunks

Copyright (c) 2025 Ronnit Peter. All rights reserved.
This software is available under a dual-license approach:
- Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0) for personal/academic use
- Commercial license available for commercial use
See LICENSE file for full terms.
"""

import os
import sys
import math
from datetime import datetime

def estimate_tokens(text):
    """
    Rough estimate of tokens (1 token ≈ 4 characters for English text)
    """
    return len(text) // 4

def split_conversation_file(input_file, max_tokens_per_chunk=30000, max_messages_per_chunk=None):
    """
    Split a conversation file into smaller chunks
    """
    print(f"📄 Splitting conversation file: {input_file}")
    print("=" * 60)
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return False
    
    # Read the file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"✅ Loaded {len(lines)} lines")
    
    # Find message lines (lines that start with a number and timestamp)
    message_lines = []
    header_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line and line[0].isdigit() and '[' in line and ']' in line:
            message_lines.append((i, line))
        else:
            header_lines.append(line)
    
    print(f"📊 Found {len(message_lines)} messages")
    
    # Create chunks
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    # Add header to first chunk
    if header_lines:
        current_chunk.extend(header_lines)
        current_chunk.append("")  # Add empty line after header
    
    for line_num, message_line in message_lines:
        # Estimate tokens for this message
        message_tokens = estimate_tokens(message_line)
        
        # Check if adding this message would exceed the limit
        if (current_tokens + message_tokens > max_tokens_per_chunk and current_chunk) or \
           (max_messages_per_chunk and len([l for l in current_chunk if l.strip() and l[0].isdigit()]) >= max_messages_per_chunk):
            # Save current chunk
            chunks.append(current_chunk)
            current_chunk = []
            current_tokens = 0
            
            # Add header to new chunk (except first line which is title)
            if header_lines:
                current_chunk.extend(header_lines[1:])  # Skip title
                current_chunk.append("")
        
        # Add message to current chunk
        current_chunk.append(message_line)
        current_chunk.append("")  # Add empty line after message
        current_tokens += message_tokens
    
    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk)
    
    print(f"✅ Created {len(chunks)} chunks")
    
    # Write chunks to files
    base_name = os.path.splitext(input_file)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for i, chunk in enumerate(chunks, 1):
        # Count messages in this chunk
        message_count = len([line for line in chunk if line.strip() and line[0].isdigit()])
        
        # Create filename
        chunk_filename = f"{base_name}_chunk_{i:02d}_of_{len(chunks):02d}_{timestamp}.txt"
        
        # Update header with chunk info
        updated_chunk = []
        for line in chunk:
            if line.startswith("📊 Total Messages:"):
                updated_chunk.append(f"📊 Total Messages: {message_count} (Chunk {i} of {len(chunks)})")
            elif line.startswith("💬 MESSAGE CONVERSATION"):
                updated_chunk.append(f"💬 MESSAGE CONVERSATION (Chunk {i} of {len(chunks)})")
            else:
                updated_chunk.append(line)
        
        # Write chunk file
        with open(chunk_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_chunk))
        
        # Calculate chunk stats
        chunk_text = '\n'.join(chunk)
        estimated_tokens = estimate_tokens(chunk_text)
        
        print(f"  📄 Chunk {i:2d}: {message_count:4d} messages, ~{estimated_tokens:5d} tokens → {chunk_filename}")
    
    return True

def create_batch_summary(input_file):
    """
    Create a summary of the batching process
    """
    base_name = os.path.splitext(input_file)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = f"{base_name}_batch_summary_{timestamp}.txt"
    
    # Find all chunk files
    chunk_files = []
    for file in os.listdir('.'):
        if file.startswith(os.path.basename(base_name)) and 'chunk_' in file and file.endswith('.txt'):
            chunk_files.append(file)
    
    chunk_files.sort()  # Sort by chunk number
    
    summary_lines = []
    summary_lines.append("📋 BATCH SUMMARY")
    summary_lines.append("=" * 60)
    summary_lines.append(f"📄 Original File: {input_file}")
    summary_lines.append(f"📊 Total Chunks: {len(chunk_files)}")
    summary_lines.append("")
    summary_lines.append("📁 Generated Files:")
    summary_lines.append("-" * 30)
    
    total_messages = 0
    total_tokens = 0
    
    for chunk_file in chunk_files:
        with open(chunk_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            messages = [line for line in lines if line.strip() and line[0].isdigit()]
            tokens = estimate_tokens(content)
            
            summary_lines.append(f"  📄 {chunk_file}")
            summary_lines.append(f"     Messages: {len(messages)}")
            summary_lines.append(f"     Tokens: ~{tokens:,}")
            summary_lines.append("")
            
            total_messages += len(messages)
            total_tokens += tokens
    
    summary_lines.append("📊 TOTAL:")
    summary_lines.append(f"  Messages: {total_messages}")
    summary_lines.append(f"  Tokens: ~{total_tokens:,}")
    summary_lines.append("")
    summary_lines.append("💡 Usage Tips:")
    summary_lines.append("  - Each chunk is optimized for GPT-4o3's 128K token context")
    summary_lines.append("  - Process chunks sequentially for chronological order")
    summary_lines.append("  - Use chunk numbers to maintain conversation flow")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_lines))
    
    print(f"✅ Batch summary saved to: {summary_file}")

def main():
    """
    Main function
    """
    print("🎯 Conversation Batcher")
    print("=" * 60)
    print("Split large conversation files into manageable chunks")
    print("")
    
    if len(sys.argv) < 2:
        print("Usage: python3 conversation_batcher.py <conversation_file> [max_tokens_per_chunk]")
print("")
print("Examples:")
print("  python3 conversation_batcher.py conversation__1234567890_20250731_134949.txt")
print("  python3 conversation_batcher.py conversation__1234567890_20250731_134949.txt 20000")
        return
    
    input_file = sys.argv[1]
    max_tokens = int(sys.argv[2]) if len(sys.argv) > 2 else 30000
    
    print(f"📄 Input file: {input_file}")
    print(f"🎯 Max tokens per chunk: {max_tokens:,}")
    print("")
    
    # Split the file
    success = split_conversation_file(input_file, max_tokens)
    
    if success:
        # Create summary
        create_batch_summary(input_file)
        print("")
        print("🎉 Batching completed successfully!")
        print("📁 Check the generated chunk files for your conversation parts.")
    else:
        print("")
        print("❌ Batching failed!")

if __name__ == '__main__':
    main() 