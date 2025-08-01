# 📱 Usage Example

## Quick Start

1. **Grant Full Disk Access to Terminal** (System Preferences → Security & Privacy → Privacy → Full Disk Access)

2. **Run the exporter with a phone number or name:**

```bash
# Export by phone number
python3 message_exporter.py +1234567890

# Export by contact name
python3 message_exporter.py "John Doe"

# Export with different phone formats
python3 message_exporter.py 1234567890
python3 message_exporter.py "(123) 456-7890"
```

3. **Check the generated files:**
   - `conversation_[contact]_[timestamp].txt` - Simple conversation
   - `detailed_conversation_[contact]_[timestamp].txt` - Detailed format
   - `summary_[contact]_[timestamp].txt` - Summary with counts

## Example Output

```
🎯 Message Exporter
============================================================
Export complete message history for any contact

🔍 Searching for: +1234567890
✅ Found contact: +1234567890
📨 Exporting messages for: +1234567890 (+1234567890)
============================================================
✅ Found 1250 messages
✅ Cleaned 1248 messages
✅ Simple conversation saved to: conversation__1234567890_20250731_134949.txt
✅ Detailed conversation saved to: detailed_conversation__1234567890_20250731_134949.txt
✅ Summary saved to: summary__1234567890_20250731_134949.txt

🎉 Export completed successfully!
📁 Check the generated files for your conversation history.
```

## Generated Files

### Simple Conversation Format
```
💬 MESSAGE CONVERSATION
============================================================
📱 Contact: +1234567890 (+1234567890)
📅 Date Range: 2024-01-15 10:30:00 to 2024-01-20 15:45:30
📊 Total Messages: 1248

  1. [2024-01-15 10:30:00] Contact: Hello, how are you?

  2. [2024-01-15 10:31:00] You: I'm doing great, thanks!

  3. [2024-01-15 10:32:00] Contact: That's wonderful to hear

  4. [2024-01-16 14:22:46] Contact: Are you free to chat later?
```

### Detailed Conversation Format
```
💬 DETAILED MESSAGE CONVERSATION
============================================================
📱 Contact: +1234567890 (+1234567890)
📅 Date Range: 2024-01-15 10:30:00 to 2024-01-20 15:45:30
📊 Total Messages: 1248

📋 CONVERSATION:
------------------------------------------------------------

  1. [2024-01-15 10:30:00]
    FROM: Contact
    TO: You
    MESSAGE: Hello, how are you?
    📱 Service: iMessage

  2. [2024-01-15 10:31:00]
    FROM: You
    TO: Contact
    MESSAGE: I'm doing great, thanks!
    📱 Service: iMessage
```

## Features

- ✅ **Complete Text Extraction**: Gets full message content
- ✅ **Multiple Search Options**: Phone number or contact name
- ✅ **Clean Output**: Removes artifacts and formatting issues
- ✅ **Chronological Order**: Messages sorted from oldest to newest
- ✅ **Sender/Receiver Info**: Shows who sent what to whom
- ✅ **Multiple Formats**: Simple, detailed, and summary formats

## Troubleshooting

- **Contact Not Found**: Try different phone number formats or exact contact name
- **Permission Errors**: Ensure Terminal has Full Disk Access
- **No Messages**: Verify the contact has message history 