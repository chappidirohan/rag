import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Send, Upload, FileText, Bot, User, Loader2 } from 'lucide-react';
import './index.css';

const App = () => {
    const [messages, setMessages] = useState([
        { role: 'bot', content: 'Hello! Upload a document and ask me anything about it.', sources: [] }
    ]);
    const [input, setInput] = useState('');
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);

    useEffect(() => {
        fetchDocuments();
    }, []);

    const fetchDocuments = async () => {
        try {
            const res = await axios.get('/api/documents');
            setDocuments(res.data);
        } catch (err) {
            console.error("Error fetching documents", err);
        }
    };

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setUploading(true);
        try {
            await axios.post('/api/documents/upload', formData);
            fetchDocuments();
        } catch (err) {
            alert("Error uploading file");
        } finally {
            setUploading(false);
        }
    };

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const res = await axios.post('/api/chat/ask', { question: input });
            const botMsg = {
                role: 'bot',
                content: res.data?.answer || "I received a blank response.",
                sources: Array.isArray(res.data?.sources) ? res.data.sources : []
            };
            setMessages(prev => [...prev, botMsg]);
        } catch (err) {
            console.error("Chat error:", err);
            setMessages(prev => [...prev, { role: 'bot', content: 'Sorry, I encountered an error connecting to the service.', sources: [] }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <div className="sidebar">
                <h2>Documents</h2>
                <label className="upload-btn">
                    {uploading ? <Loader2 className="animate-spin" size={20} /> : <Upload size={20} />}
                    {uploading ? 'Processing...' : 'Upload Document'}
                    <input type="file" hidden onChange={handleUpload} accept=".pdf,.docx,.txt" />
                </label>

                <div className="doc-list">
                    {documents.map((doc) => (
                        <div key={doc.id} className="doc-item">
                            <FileText size={16} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                            {doc.name}
                        </div>
                    ))}
                    {documents.length === 0 && <p style={{ color: 'var(--text-dim)', fontSize: '0.875rem' }}>No documents uploaded yet.</p>}
                </div>
            </div>

            <div className="chat-area">
                <div className="messages">
                    {messages.map((msg, i) => (
                        <div key={i} className={`message ${msg.role === 'user' ? 'user-message' : 'bot-message'}`}>
                            <div style={{ display: 'flex', gap: '8px', marginBottom: '4px' }}>
                                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                                <strong>{msg.role === 'user' ? 'You' : 'AI Assistant'}</strong>
                            </div>
                            <div>{msg.content}</div>
                            {msg.sources && msg.sources.length > 0 && (
                                <span className="source-tag">Source: {msg.sources.join(', ')}</span>
                            )}
                        </div>
                    ))}
                    {loading && (
                        <div className="message bot-message">
                            <Loader2 className="animate-spin" size={20} />
                        </div>
                    )}
                </div>

                <div className="input-container">
                    <div className="input-box">
                        <input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask a question about your documents..."
                            disabled={loading}
                        />
                        <button className="send-btn" onClick={handleSend} disabled={loading}>
                            <Send size={18} />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default App;
