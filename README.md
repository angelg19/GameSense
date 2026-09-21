# 🎮 GameSense Player Insights Platform

A full-stack AI-powered platform for gamers, providing deep insights into leveling up their gameplay by importing their real stats and displaying personalized tips. Built with **Python**, **TypeScript**, **OpenAI LLMs**, **RAG**, and **Pinecone**.

---

## Features

### Sleek and Efficient User Dashboard
- Provides all the users stats in an organized format, which can be earily viewed by navigating through tabs. 
- Calculates additional useful stats such as win percentage on maps / heroes, or accuracy and average KD ratio.
- Generates an overview on what stats to focus on based on your entire profile, and what current strengths are.
- Allows users to type their own questions to gain better understanding on their profile and gain more insight on how to improve.

### Semantic Search for Enhanced Personalization
- Uses semantic search in vector db to find game information and stats most related to user questions.

### Modern Full-Stack Architecture
- Built on **Next.js App Router** with server components and API routes.
- Type-safe frontend with **TypeScript**.
- Simplified backend with **Python Flask API**

---

## 🛠️ Tech Stack

### Frontend
- Next.js (App Router)
- TypeScript
- Tailwind CSS

### Backend
- Flask API Routes

### AI / RAG
- OpenAI GPT models
- Vector embeddings
- Semantic search + RAG pipeline

---

## Project Structure
/backend (python)
    /routes → flask api routes
    /services → update csv files, vector database
/data
    /csv files → various webscraped sources to supply vector database with game knowledge
/frontend (typescript)
    /components → UI components
    /home → homepage structure and main stats view page

---

## 🚀 How It Works

### 1. User Searches For Account
Users provide either an account name or id for the game Marvel Rivals.

### 2. System Performs Retrieval
Uses external API to retrieve their in game stats, match history, hero stats, and more.

### 3. Easy to Digest Dashboard
- Dashboard displays all user stats in an easy to read fashion and provides simple analysis.
- Performances on Heroes, Maps, Game modes are broken down by category.

### 4. LLM Generates In-depth Analysis
- LLM uses player stats and additional information from vector database to provide insights on becoming a better player.
- Info from vector database comes from various sources including youtube video transcripts, official Marvel Rivals site, webscraped leaderboard data.
- Ask LLM further questions about tips for the game to gain more insight on how to become better player.

---

## Future Enhancements
- Accounts for quick access / lookups 
- Deeper information database for advanced tips based on player level
- Potential expansion to other games besides Marvel Rivals

---

## Getting Started

Deployed site currently pending. Install project to use locally.
