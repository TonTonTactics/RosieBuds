# The Webapp

## Overview

The Webapp is a frontend built with React and Vite that interacts
with the Hub backend API to display data.


## Requirements

Make sure Node.js is installed --> [here](https://nodejs.org/en/download/)

To install required dependencies, run the following command in your terminal:

```bash
cd webapp
npm install
```

## Structure

```
src/
│
├── App.jsx          # Main React app component
├── Dashboard.jsx    # Dashboard UI
├── Dashboard.css
├── Fetch.jsx        # Fetching data from the Hub API
├── Game.jsx         # Tic-Tac-Toe game component (mini-game)
├── Game.css
├── Guidebook.jsx    # Guidebook UI component
├── Guidebook.css
├── index.css        # Global CSS styles
├── main.jsx         # Entry point
├── Routes.jsx       # Defines app routing and page navigation
├── Start.jsx        # landing page of the app
├── Start.css
└── styles.css       # Component-specific styles
```

## How to Run
For Development (must be in Webapp folder):
```bash
npm run dev
```

For Production:
```bash
npm run build     # Builds optimized production files
npm run preview   # Serves the production build locally for testing
```

[After running, visit: http://localhost:5173](http://localhost:5173)

## Resources

For more information, please check out the following documents:
- [React](https://react.dev/learn)
- [Routes](https://www.w3schools.com/react/react_router.asp)
- [JSX](https://www.w3schools.com/react/react_jsx.asp)
- [Node.js](https://nodejs.org/docs/latest/api/)
- [fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#making_a_request)
- [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
