# Agent Icons

The agent manifest references two icon files:
- `icon-outline.png` - Outline icon (32x32px recommended)
- `icon-color.png` - Color icon (192x192px recommended)

## Creating Icons

You can create your own icons or use placeholders. Here are the requirements:

### Icon Specifications

**Outline Icon (`icon-outline.png`)**:
- Size: 32x32 pixels
- Format: PNG with transparency
- Style: Simple line drawing, monochrome
- Use: Displayed in Teams app bar and other UI elements

**Color Icon (`icon-color.png`)**:
- Size: 192x192 pixels
- Format: PNG
- Style: Full color, represents your brand
- Use: Displayed in Teams app catalog and details pages

### Quick Icon Ideas for Dad Joke Agent

- A smiling face with a dad mustache
- A classic "groan" emoji style face
- Speech bubble with "😄" inside
- Retro microphone icon

### Tools for Creating Icons

- **Figma** (free): https://figma.com
- **Canva** (free templates): https://canva.com
- **DALL-E or MidJourney**: Generate with AI
- **Favicon.io**: Simple text-based icons

### Temporary Placeholder

Until you create proper icons, you can:
1. Use emoji as text-based icons
2. Generate simple geometric shapes
3. Use Microsoft's default bot icon template
4. Download free icons from https://icons8.com or https://flaticon.com

### Icon File Paths

Place your icon files in the same directory as `agent-manifest.json`:
```
Dad joke Agent example/
├── icon-outline.png
├── icon-color.png
└── agent-manifest.json
```

The manifest already references these files, so once you add them, they'll work automatically.
