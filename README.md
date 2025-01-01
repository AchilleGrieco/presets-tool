# Preset Text Tool 🚀

A powerful and customizable tool that allows you to quickly insert predefined text templates in any application using hotkeys. Perfect for content creators, customer service representatives, or anyone who frequently uses repetitive text patterns.

## Features ✨

- 🎯 **Global Hotkeys**: Access your templates from any application
- 🗔**Window-Specific Templates**: Different templates for different applications
- 🌗 **Dark Theme Interface**: Easy on the eyes
- ⚡ **Quick Search**: Instantly find and insert your templates
- 🔧 **Customizable Templates**: Easy to create and modify JSON template files

## Installation 🔧

1. Ensure you have Python 3.6+ installed on your system
2. Install the required dependencies:
```bash
pip install pyperclip keyboard pygetwindow pywin32
```

## Usage 🎮

### Hotkeys
- `Ctrl + Alt + I`: Open the template selector
- `Ctrl + I`: Add new entry in the template

### Basic Usage
1. Start the application by running `preset_tool.py`
2. When you need to select a text:
   - Press `Ctrl + Alt + I`
   - Type the keyword for your text
   - Press Enter to copy the text

## Template Setup 📝

Text templates are stored in JSON files in the `templates` folder. Each template file should follow this structure:

template_names are the strings that appear in the window name you have opened, when pressing the hotkey combination with the window selected you have access to the text templates stored in "templates" dictionary for that specific window.

```json
{
    "template_names": ["ApplicationName", "alternative.name"],
    "templates": {
        "keyword1": "Your template text here",
        "keyword2": "Another template text"
    }
}
```

### Example Template (youtube.json)
```json
{
    "template_names": ["YouTube", "youtube.com"],
    "templates": {
        "thanks": "Thank you for watching! Don't forget to like and subscribe for more content.",
        "intro": "Hey everyone! Welcome back to my channel.",
        "comment": "Thanks for your comment! Really appreciate your feedback.",
        "timestamps": "Timestamps:\n0:00 - Intro\n1:30 - Main Topic\n5:00 - Summary\n6:00 - Outro",
        "pinned": "Pinned comment: Thanks for watching! Let me know your thoughts in the comments below 👇"
    }
}
```

### Creating New Templates

1. Create a new JSON file in the `templates` folder
2. Name it according to the application (e.g., `outlook.json`, `discord.json`)
3. Follow the template structure above:
   - `template_names`: Array of window titles that should trigger these templates
   - `templates`: Dictionary of keyword-text pairs

## Tips 💡

- Keep keywords short and memorable
- Use descriptive template names that match your window titles
- You can use `\n` for new lines in your templates

## Troubleshooting 🔍

- If templates aren't showing up, check if at least part of the window title matches any of your `template_names`
- Ensure your JSON files are properly formatted
- Check if the `templates` folder exists in the same directory as the script

## Contributing 🤝

Feel free to fork this project and submit pull requests with improvements.

## License 📄

This project is open source and available under the MIT License.
