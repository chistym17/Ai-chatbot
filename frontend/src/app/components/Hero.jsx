// src/components/HeroSection.js
import React from 'react';
import { FaRobot, FaDatabase, FaComments } from 'react-icons/fa';

const HeroSection = () => {
    return (
        <div className="bg-gradient-to-r from-blue-400 to-purple-500 text-white h-screen flex flex-col justify-center items-center text-center">
            <h1 className="text-5xl font-bold mb-6">Your AI Medical Assistant</h1>
            <p className="text-lg mb-8">Ask questions in plain English, and get SQL commands to query complex medical data.</p>
            <div className="flex space-x-10">
                <div className="flex flex-col items-center">
                    <FaRobot className="text-6xl mb-2" />
                    <span>AI-Powered</span>
                </div>
                <div className="flex flex-col items-center">
                    <FaDatabase className="text-6xl mb-2" />
                    <span>Data Insights</span>
                </div>
                <div className="flex flex-col items-center">
                    <FaComments className="text-6xl mb-2" />
                    <span>Interactive Queries</span>
                </div>
            </div>
        </div>
    );
};

export default HeroSection;