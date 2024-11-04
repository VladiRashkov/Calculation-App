import React, { useState, useEffect } from 'react';

function RequestsList({ setIsLoggedIn }) {
    const [requests, setRequests] = useState([]);
    const [selectedRequest, setSelectedRequest] = useState(null);
    const [results, setResults] = useState([]);
    const [loadingRequests, setLoadingRequests] = useState(true);
    const [loadingResults, setLoadingResults] = useState(false);
    const [error, setError] = useState(null);

    
    useEffect(() => {
        const fetchRequests = async () => {
            setLoadingRequests(true); 
            try {
                const res = await fetch("http://localhost:8000/admin/requests", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });

                
                if (!res.ok) {
                    throw new Error("Failed to fetch requests");
                }

                
                const data = await res.json();
                setRequests(Array.isArray(data) ? data : []); 
            } catch (error) {
                setError(error.message); 
            } finally {
                setLoadingRequests(false); 
            }
        };

        fetchRequests(); 
    }, []); 

    
    const loadResults = (requestId) => {
        setLoadingResults(true); 
        fetch(`http://localhost:8000/admin/results/${requestId}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}` 
            }
        })
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Failed to fetch results");
                }
                return res.json(); 
            })
            .then((data) => {
                setSelectedRequest(requestId); 
                setResults(Array.isArray(data) ? data : []); 
            })
            .catch((error) => setError(error.message)) 
            .finally(() => setLoadingResults(false)); 
    };

    
    const handleLogout = () => {
        localStorage.removeItem('token'); 
        setIsLoggedIn(false); 
    };

    return (
        <div>
            <h2>Your Requests</h2>
            <button onClick={handleLogout}>Logout</button>
            {loadingRequests ? (
                <p>Loading requests...</p> 
            ) : error ? (
                <p style={{ color: "red" }}>{error}</p> 
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Request Name</th>
                            <th>File Reference</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {requests.map((request) => (
                            <tr key={request.id}>
                                <td>{request.request_name}</td>
                                <td>{request.file_reference}</td>
                                <td>
                                    <button onClick={() => loadResults(request.id)}>
                                        View Results
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            {selectedRequest && ( 
                <div>
                    <h3>Results for Request ID: {selectedRequest}</h3>
                    {loadingResults ? (
                        <p>Loading results...</p> 
                    ) : (
                        <ul>
                            {results.map((result) => (
                                <li key={result.id}>Result Value: {result.result_value}</li>
                            ))}
                        </ul>
                    )}
                </div>
            )}
        </div>
    );
}

export default RequestsList;
