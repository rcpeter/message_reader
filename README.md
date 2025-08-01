# 📱 macOS Message Exporter

A streamlined tool to export complete message history from macOS Messages app for any contact.

## 🚀 Quick Start

### Prerequisites
- macOS with Messages app
- Python 3.6+
- Full Disk Access granted to Terminal (System Preferences → Security & Privacy → Privacy → Full Disk Access)

### Usage

```bash
# Export by phone number
python3 message_exporter.py +1234567890

# Export by contact name
python3 message_exporter.py "John Doe"

# Export with different phone formats
python3 message_exporter.py 1234567890
python3 message_exporter.py "(123) 456-7890"
```

## 📋 Features

- ✅ **Complete Text Extraction**: Extracts full message content from `attributedBody` field
- ✅ **Multiple Search Options**: Search by phone number or contact name
- ✅ **Clean Output**: Removes binary artifacts and formatting issues
- ✅ **Multiple Formats**: Generates simple, detailed, and summary formats
- ✅ **Chronological Order**: Messages sorted from oldest to newest
- ✅ **Sender/Receiver Info**: Clearly shows who sent what to whom

## 📁 Output Files

For each export, the tool generates three files:

1. **`conversation_[contact]_[timestamp].txt`** - Simple conversation format
2. **`detailed_conversation_[contact]_[timestamp].txt`** - Detailed format with sender/receiver info
3. **`summary_[contact]_[timestamp].txt`** - Summary with message counts

## 🔧 Setup

### 1. Grant Full Disk Access
1. Open System Preferences
2. Go to Security & Privacy → Privacy
3. Select "Full Disk Access" from the left sidebar
4. Click the lock icon and enter your password
5. Add Terminal (or your terminal app) to the list

### 2. Run the Exporter
```bash
# Navigate to the message_exporter directory
cd /path/to/message_exporter

# Export messages for a contact
python3 message_exporter.py +1234567890
```

## 📊 Example Output

```
💬 MESSAGE CONVERSATION
============================================================
📱 Contact: +1234567890 (+1234567890)
📅 Date Range: 2024-01-15 10:30:00 to 2024-01-20 15:45:30
📊 Total Messages: 25

  1. [2024-01-15 10:30:00] Contact: Hello, how are you?

  2. [2024-01-15 10:31:00] You: I'm doing great, thanks!

  3. [2024-01-15 10:32:00] Contact: That's wonderful to hear

  4. [2024-01-16 14:22:46] Contact: Are you free to chat later?

  5. [2024-01-16 14:32:06] You: Sure, I'll be available

  6. [2024-01-17 14:29:07] You: How's your day going?

  7. [2024-01-18 14:00:01] You: Great news, I got the job!

  8. [2024-01-20 14:24:47] You: Looking forward to starting next week
```

## 🔍 Troubleshooting

### Contact Not Found
- Try different phone number formats
- Use the exact contact name as it appears in Messages
- Check if the contact has any message history

### Permission Errors
- Ensure Terminal has Full Disk Access
- Restart Terminal after granting permissions
- Check if Messages app is installed and has data

### No Messages Found
- Verify the contact has message history
- Check if Messages app has been used
- Ensure the database file exists at `~/Library/Messages/chat.db`

## 🛠 Technical Details

### Database Location
- Messages database: `~/Library/Messages/chat.db`
- SQLite3 database with message history

### Text Extraction
- Extracts from `attributedBody` field (NSAttributedString format)
- Cleans binary artifacts and formatting issues
- Preserves complete message content

### Supported Formats
- Phone numbers: `+1234567890`, `(123) 456-7890`, `1234567890`
- Contact names: Exact names as stored in Messages

## 📝 License

This tool is available under a **dual-license** approach:

### 🎓 **Personal & Academic Use**
Available under **Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)**
- ✅ **Personal Use**: You can use this tool for your own message export needs
- ✅ **Academic Use**: Educational and research purposes are permitted
- ✅ **Modifications**: You can modify and improve the software
- ❌ **Commercial Use**: Not permitted under this license

### 💼 **Commercial Use**
Requires a separate commercial license agreement with the copyright holder.

**See [LICENSE](LICENSE) for full terms and contact information for commercial licensing.**

Please respect privacy and only export your own messages.

## 🤝 Contributing

Feel free to submit issues or improvements. The tool is designed to be simple and user-friendly.

---

**Note**: This tool only works on macOS and requires access to the Messages database. Always ensure you have permission to export the messages you're accessing. 