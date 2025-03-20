'use client';
import { useState } from 'react';
import ChatWidget from './ChatWidget';

export default function ChatInfo() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className="relative min-h-[600px]">
      <div className="max-w-6xl mx-auto p-12 rounded-3xl bg-gradient-to-br from-blue-50 to-indigo-50 shadow-xl my-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          AI-Powered Healthcare Assistant
        </h2>
        
        <div className="space-y-8 max-w-5xl mx-auto">
          <div className="flex items-start gap-6 p-6 bg-white/50 rounded-2xl hover:bg-white/70 transition-colors">
            <div className="p-4 bg-blue-100 rounded-xl">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h3 className="text-2xl font-semibold text-gray-800 mb-3">Quick Data Retrieval</h3>
              <p className="text-gray-600 text-lg leading-relaxed">Get instant access to patient records, appointments, and medical information through natural language queries.</p>
            </div>
          </div>

          <div className="flex items-start gap-6 p-6 bg-white/50 rounded-2xl hover:bg-white/70 transition-colors">
            <div className="p-4 bg-blue-100 rounded-xl">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div>
              <h3 className="text-2xl font-semibold text-gray-800 mb-3">Complex Queries Made Simple</h3>
              <p className="text-gray-600 text-lg leading-relaxed">Ask questions in plain English and get accurate, structured responses from our healthcare database.</p>
            </div>
          </div>

          <div className="flex items-start gap-6 p-6 bg-white/50 rounded-2xl hover:bg-white/70 transition-colors">
            <div className="p-4 bg-blue-100 rounded-xl">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h3 className="text-2xl font-semibold text-gray-800 mb-3">Example Queries</h3>
              <ul className="text-gray-600 text-lg space-y-3 list-disc list-inside">
                <li>"Show me all appointments for Dr. Smith this week"</li>
                <li>"Find patients with diabetes in the last month"</li>
                <li>"List all hospitals in the northern region"</li>
                <li>"Show me the medical records for patient ID 12345"</li>
                <li>"What are the common treatments for hypertension?"</li>
              </ul>
            </div>
          </div>
        </div>

        <button
          onClick={toggleChat}
          className="mt-12 px-8 py-4 bg-blue-600 text-white text-lg rounded-xl hover:bg-blue-700 transition-colors flex items-center gap-3 mx-auto shadow-lg hover:shadow-xl"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          Try the AI Assistant
        </button>
      </div>

      <ChatWidget isOpen={isChatOpen} onClose={toggleChat} />
    </div>
  );
} 