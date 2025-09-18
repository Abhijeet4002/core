# Django Blog Platform - Code Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO BLOG PLATFORM                     │
│                     Architecture Overview                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FRONTEND      │    │   DJANGO CORE   │    │   DATABASE      │
│   (Templates)   │◄──►│   (Backend)     │◄──►│   (SQLite/PG)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └─────────────►│  WEBSOCKETS     │              │
                        │  (Channels)     │              │
                        └─────────────────┘              │
                                 │                        │
                        ┌─────────────────┐              │
                        │  STATIC FILES   │              │
                        │  (Media/CSS)    │              │
                        └─────────────────┘              │

═══════════════════════════════════════════════════════════════

                        DETAILED ARCHITECTURE

┌──────────────────────────────────────────────────────────────┐
│                    REQUEST/RESPONSE FLOW                     │
└──────────────────────────────────────────────────────────────┘

   User Request
       ↓
┌─────────────────┐
│   Django URLs   │  ← core/urls.py + blog/urls.py
└─────────────────┘
       ↓
┌─────────────────┐
│   Middleware    │  ← SubscriptionMiddleware (Premium Check)
└─────────────────┘
       ↓
┌─────────────────┐
│     Views       │  ← Class-Based & Function-Based Views
└─────────────────┘
       ↓
┌─────────────────┐
│     Models      │  ← User, Profile, Post, Comment, Like
└─────────────────┘
       ↓
┌─────────────────┐
│   Templates     │  ← HTML with Django Template Language
└─────────────────┘
       ↓
   HTTP Response

═══════════════════════════════════════════════════════════════

                          MODEL RELATIONSHIPS

┌─────────────┐    OneToOne    ┌─────────────┐
│    User     │◄──────────────►│   Profile   │
│ (Custom)    │                │ (Subscription)│
└─────────────┘                └─────────────┘
      │                               │
      │ ForeignKey                    │ ManyToMany
      │ (Author)                      │ (Follows)
      ↓                               ↓
┌─────────────┐                ┌─────────────┐
│    Post     │                │    User     │
│ (Blog)      │                │ (Self-ref)  │
└─────────────┘                └─────────────┘
      │                               
      │ ForeignKey                    
      ├─────────────────┐             
      ↓                 ↓             
┌─────────────┐   ┌─────────────┐     
│   Comment   │   │    Like     │     
│ (Thread)    │   │ (Toggle)    │     
└─────────────┘   └─────────────┘     

═══════════════════════════════════════════════════════════════

                        FEATURE BREAKDOWN

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   AUTHENTICATION │  │    CONTENT       │  │   REAL-TIME      │
│                  │  │   MANAGEMENT     │  │   FEATURES       │
│ • Custom User    │  │                  │  │                  │
│ • Email Login    │  │ • CRUD Posts     │  │ • WebSockets     │
│ • Role-Based     │  │ • Rich Editor    │  │ • Live Comments  │
│ • Registration   │  │ • Image Upload   │  │ • Instant Updates│
│ • Permissions    │  │ • Categories     │  │ • Group Messaging│
└──────────────────┘  │ • Tags           │  └──────────────────┘
                      │ • SEO Slugs      │
┌──────────────────┐  └──────────────────┘  ┌──────────────────┐
│   SUBSCRIPTION   │                        │    SOCIAL        │
│     SYSTEM       │  ┌──────────────────┐  │   FEATURES       │
│                  │  │      ADMIN       │  │                  │
│ • Paywall Logic  │  │    INTERFACE     │  │ • Like System    │
│ • Premium Access │  │                  │  │ • Comment Thread │
│ • Date Tracking  │  │ • Django Admin   │  │ • User Profiles  │
│ • Subscription   │  │ • Custom Models  │  │ • Follow System  │
│ • Middleware     │  │ • Bulk Actions   │  │ • Social Login   │
└──────────────────┘  └──────────────────┘  └──────────────────┘

═══════════════════════════════════════════════════════════════

                         TECHNOLOGY STACK

┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                              │
├─────────────────────────────────────────────────────────────┤
│ Django 5.2          │ Web Framework                         │
│ Django Channels     │ WebSocket Support                     │
│ SQLite/PostgreSQL   │ Database                             │
│ Pillow             │ Image Processing                      │
│ django-taggit      │ Tagging System                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
├─────────────────────────────────────────────────────────────┤
│ Django Templates    │ Server-Side Rendering                │
│ Tailwind CSS       │ Utility-First Styling               │
│ Vanilla JavaScript │ AJAX & WebSocket Client              │
│ HTML5/CSS3         │ Modern Web Standards                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      DEPLOYMENT                             │
├─────────────────────────────────────────────────────────────┤
│ ASGI Server        │ WebSocket Support (Daphne)           │
│ WSGI Server        │ Traditional HTTP (Gunicorn)          │
│ Static Files       │ Collectstatic + CDN Ready           │
│ Media Files        │ User Uploads Handling                │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

                         SECURITY FEATURES

┌─────────────────────────────────────────────────────────────┐
│ ✓ CSRF Protection    │ All forms protected                 │
│ ✓ SQL Injection      │ ORM prevents raw queries            │
│ ✓ XSS Protection     │ Template auto-escaping              │
│ ✓ Authentication     │ Login required decorators           │
│ ✓ Authorization      │ Permission-based access             │
│ ✓ File Upload        │ Secure media handling               │
│ ✓ Session Security   │ Secure session configuration        │
│ ✓ Password Hashing   │ Django's robust password system     │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

                      PERFORMANCE OPTIMIZATIONS

┌─────────────────────────────────────────────────────────────┐
│ Database Indexing   │ Foreign Keys & Search Fields         │
│ Query Optimization  │ Select_related & Prefetch_related     │
│ Template Caching    │ Fragment caching ready               │
│ Static File Serving │ Efficient file delivery              │
│ AJAX Requests       │ Reduce page reloads                  │
│ WebSocket Groups    │ Targeted real-time updates           │
└─────────────────────────────────────────────────────────────┘