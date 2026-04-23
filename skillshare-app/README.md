# SkillShare Friends App

A fun and interactive React application for skill swapping between friends. Users can match with others based on skills they want to learn and teach, chat, and even video call using Jitsi Meet.

## Features

- **User Profiles**: Create a profile with skills you can teach and want to learn
- **Skill Matching**: Automatically find friends who match your skill swap interests
- **Real-time Chat**: Chat with matched friends
- **Video Calls**: Start video calls using Jitsi Meet integration
- **Gamification**: Earn scores and badges for learning activities
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **React 19** with TypeScript
- **Vite** for build tooling
- **Lucide React** for icons
- **Tailwind CSS** for styling (via inline styles)
- **Jitsi Meet** for video calls

## Getting Started

### Prerequisites

- Node.js (version 18 or higher)
- npm or yarn

### Installation

1. Clone or download the project files
2. Navigate to the project directory
3. Install dependencies:

```bash
npm install
```

### Running the App

Start the development server:

```bash
npm run dev
```

Open your browser and go to `http://localhost:5173`

### Building for Production

```bash
npm run build
```

### Linting

```bash
npm run lint
```

## Project Structure

```
skillshare-app/
├── src/
│   ├── App.tsx          # Main application component
│   ├── main.tsx         # Entry point
│   ├── index.css        # Global styles
│   └── assets/          # Static assets
├── package.json         # Dependencies and scripts
├── vite.config.ts       # Vite configuration
├── tsconfig.json        # TypeScript configuration
└── README.md            # This file
```

## How It Works

1. **Login**: Click "Come Play!" to enter the app with a mock profile
2. **View Profile**: See your skill score, badges, and what you can teach/learn
3. **Find Matches**: The app shows friends who have complementary skills
4. **Connect**: Chat or video call with matched friends
5. **Learn**: Use the video calls to teach and learn skills

## Key Components

- **App**: Main component managing state and routing
- **MagicCall**: Video call component using Jitsi Meet iframe
- **User Interface**: Responsive design with playful colors and animations

## Customization

- Modify `MOCK_USERS` in `App.tsx` to add more users
- Change colors by updating the hex codes in the component styles
- Add more quotes to the `QUOTES` array for variety

## Troubleshooting

- **Video calls not working**: Ensure your browser allows camera/microphone access
- **Build errors**: Make sure all dependencies are installed with `npm install`
- **TypeScript errors**: Check that all interfaces match the data structures

## Learning Resources

This app demonstrates:
- React hooks (useState, useEffect)
- TypeScript interfaces
- Component composition
- Event handling
- Conditional rendering
- Array methods (filter, map)
- CSS-in-JS styling
- Integration with external services (Jitsi)

Feel free to explore the code, modify it, and use it as a starting point for your own skill-sharing platform!
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
