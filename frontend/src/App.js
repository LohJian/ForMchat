import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProfilePage from './components/ProfilePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<h1>Home Page</h1>} />
        <Route path="/profile" element={<ProfilePage />} />   
      </Routes>
    </Router>
  );
}

export default App;
