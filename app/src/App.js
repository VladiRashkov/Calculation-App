import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import Register from './Register';
import Login from './Login';
import RequestsList from './RequestList';
import './App.css'

function LogoutButton({ setIsLoggedIn }) {
    const navigate = useNavigate();

    const handleLogout = () => {
        
        localStorage.removeItem('token');
        setIsLoggedIn(false);
        navigate('/login'); 
    };

    return <button onClick={handleLogout}>Logout</button>;
}

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false); 
    const openRequestsList = () => {
        
        window.open('/requests', '_blank');
    };

    return (
        <Router>
            <div className="App">
                <h1>Admin Panel</h1>
                <nav>
                    <ul>
                        <li>
                            <Link to="/login">Login</Link>
                        </li>
                        <li>
                            <Link to="/register">Register</Link>
                        </li>
                        <li>
                            <button onClick={openRequestsList}>Open My Requests</button>
                        </li>
                        {isLoggedIn && <li><LogoutButton setIsLoggedIn={setIsLoggedIn} /></li>}
                    </ul>
                </nav>
                <Routes>
                    <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/requests" element={<RequestsList setIsLoggedIn={setIsLoggedIn} />} /> {/* Pass setIsLoggedIn here */}
                </Routes>
            </div>
        </Router>
    );
}

export default App;
//ammended