import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Home.css";

function Home() {
  const [message, setMessage] = useState("");
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URLS = {
    helloService: process.env.REACT_APP_HELLO_SERVICE_URL || 'http://localhost:3001',
    profileService: process.env.REACT_APP_PROFILE_SERVICE_URL || 'http://localhost:3002'
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [helloRes, profileRes] = await Promise.all([
          axios.get(`${API_URLS.helloService}/`),
          axios.get(`${API_URLS.profileService}/fetchUser`)
        ]);

        // Handle hello-service response (supports both {msg} and direct string)
        const helloData = helloRes.data;
        setMessage(typeof helloData === 'object' ? helloData.msg || helloData.message : helloData);

        // Handle profile service response (ensure it's always an array)
        setProfiles(Array.isArray(profileRes.data) ? profileRes.data : []);
        
      } catch (err) {
        setError(err.response?.data?.message || err.message || "Failed to load data");
        console.error("API Error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [API_URLS.helloService, API_URLS.profileService]);

  if (loading) return <div className="loading">Loading data...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="home-container">
      <header>
        <h1>{message || "Welcome to MERN Microservices"}</h1>
      </header>
      
      <section className="profiles-section">
        <h2>User Profiles</h2>
        <div className="profiles-grid">
          {profiles.length > 0 ? (
            profiles.map((user) => (
              <div key={user._id} className="profile-card">
                <h3>{user.name}</h3>
                <p>Age: {user.age}</p>
                <p>Joined: {new Date(user.createdAt).toLocaleDateString()}</p>
              </div>
            ))
          ) : (
            <p className="no-profiles">No profiles found</p>
          )}
        </div>
      </section>
    </div>
  );
}

export default Home;