# Chademy
## 📌 **Phase 1: MVP (Minimum Viable Product) – Foundation**

🔧 **Goal**: Get a fully functional core system running to validate the concept.

### Key Deliverables:

* **User Authentication** (OAuth, Email/Password for tutors & students)
* **Landing Page** (basic version)
* **Tutor Dashboard**

  * Create Course (title, description, thumbnail)
  * Upload video (manual transcript option for now)
* **Student Dashboard**

  * Browse course catalog
  * Enroll in a course
  * Watch video (without AI transcript for now)
* **Basic Real-Time Chat** (one course room, WebSocket-based)
* **Database Models**: User, Course, Video, Enrollment, Message

### Stack Suggestions:

* Backend: Django
* Frontend: Tailwind CSS
* Real-time: Socket.IO (Node) or Django Channels
* DB: PostgreSQL


---

## 🤖 **Phase 2: AI-Powered Learning Experience**

🔧 **Goal**: Automate learning enhancement using AI and improve interactivity.

### Key Deliverables:

* **AI Video Transcription** (using Whisper API, AssemblyAI, or Azure)
* **Auto-Synced Transcript Viewer** (highlighting sentences in real time)
* **Transcript Search** (search inside videos)
* **Transcript Download** (PDF/Word)
* **Improved Real-Time Chat**

  * Replies, threads
  * Tutor-only announcement mode


---

## 💳 **Phase 3: Monetization & Tutor Empowerment**

🔧 **Goal**: Allow tutors to earn, and platform to generate revenue.

### Key Deliverables:

* **Payment Integration**

  * Stripe/PayPal for course purchase
  * Razorpay for South Asia
* **Course Pricing & Discounts**
* **Tutor Earnings Dashboard**
* **Student Purchase History**
* **Enrollment Access Control**

  * Locked courses until purchase


---

## 🧩 **Phase 4: UI/UX & 3D Landing Page Upgrade**

🔧 **Goal**: Make Learnix visually stunning, interactive, and modern.

### Key Deliverables:

* **Immersive 3D Landing Page**

  * Interactive WebGL/Three.js elements
  * Scroll-based storytelling (GSAP)
  * Tutor/student showcase animations
* **Dark Mode + Mobile Responsiveness**
* **Better Course Cards** with hover animations
* **Tutor Profiles** with ratings, testimonials


---

## 🚀 **Phase 5: Optimization, Scaling & Community Features**

🔧 **Goal**: Prepare platform for public launch and high traffic.

### Key Deliverables:

* **Progress Tracker** for students
* **Course Comments / Discussion Forum**
* **Email Notifications**

  * Enrollment confirmation
  * Chat mentions / Announcements
* **Video Compression & CDN Integration**
* **Server Load Optimization**

  * Caching, rate limiting, analytics


---

## 📌 **Optional Future Add-ons**

* AI Tutor Assistant (Q\&A on transcript)
* Group video calls / live sessions
* Certification engine
* App version (React Native or Flutter)

---

### ✅ **Summary Timeline Overview**

| Phase   | Focus                     | Duration  |
| ------- | ------------------------- | --------- |
| Phase 1 | MVP Core System           | 4–6 Weeks |
| Phase 2 | AI Features & Transcripts | 3–4 Weeks |
| Phase 3 | Monetization              | 2–3 Weeks |
| Phase 4 | UI/UX + 3D Design         | 3–4 Weeks |
| Phase 5 | Scaling & Community       | 3–5 Weeks |

---

## 🧠 Team Roles Suggestion (for Agile Dev)

* **Frontend Devs** (React, Tailwind, GSAP, Three.js)
* **Backend Devs** (Django/Node, REST APIs, DB models)
* **AI/ML Engineer** (transcription system)
* **DevOps** (deployment, optimization, monitoring)
* **UI/UX Designer** (landing page, dashboards)
* **Project Manager** (task distribution, agile flow)

---

