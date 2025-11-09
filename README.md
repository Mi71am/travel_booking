# Travel Booking System

## Project Structure

This is a collaborative Django project for managing travel bookings, reviews, payments, and user profiles. The project is organized into several apps, each with a specific purpose and set of features:

### Apps Overview

#### 1. core
**Purpose:** Provides shared templates, base layout, and static files for the entire project.
**Features:**
- Base HTML templates (header, footer, navigation)
- Shared static files (CSS, JS)
- Home and about pages

#### 2. users
**Purpose:** Manages user authentication, registration, and profiles.
**Features:**
- Signup, login, logout
- User dashboard
- Profile management (including profile pictures)

#### 3. bookings
**Purpose:** Handles trip bookings and booking management.
**Features:**
- Create, view, and manage bookings
- Booking summary and history
- Forms for booking trips

#### 4. destinations
**Purpose:** Manages travel destinations and related content.
**Features:**
- Add, edit, and list destinations
- Destination details and images
- Sample data seeding for destinations

#### 5. payments
**Purpose:** Processes payments for bookings.
**Features:**
- Payment forms and history
- Integration with booking workflow
- Payment method management

#### 6. reviews
**Purpose:** Allows users to review destinations and trips.
**Features:**
- Submit and view reviews
- Rating system



## Getting Started

1. Clone the repository
2. Set up your Python virtual environment
3. Install dependencies
4. Run migrations
5. Start the development server
