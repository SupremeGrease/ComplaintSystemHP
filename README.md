# Complaint System Backend API Documentation

This document provides an overview of the API endpoints for the Complaint System backend.

## Base URL

`http://127.0.0.1:8000/api/`

## Authentication

The API uses SessionAuthentication and BasicAuthentication. For development and testing, `AllowAny` permissions are currently enabled (`rest_framework.permissions.AllowAny`).

## Media and Static Files

*   **Media URL:** `/media/`
*   **Media Root:** `complaintsystem/media/` (where uploaded files like complaint images and QR codes are stored)
*   **Static URL:** `/static/`
*   **Static Root:** `complaintsystem/staticfiles/`

## API Endpoints

### 1. Rooms

Manage room details and QR codes.

*   **List all rooms:**
    *   `GET /api/rooms/`
*   **Create a new room:**
    *   `POST /api/rooms/`
    *   **Body:** JSON object with room details (e.g., `bed_no`, `room_no`, `Block`, `Floor_no`, `ward`, `speciality`, `room_type`, `status`).
    *   **Note:** This will automatically generate a QR code for the room, including an HMAC signature for tamper-proofing the QR data.
*   **Retrieve a single room:**
    *   `GET /api/rooms/{id}/`
    *   **Response includes:** Room details, `qr_code` URL, and `dataenc` (base64 encoded room data).
*   **Update a room (full update):**
    *   `PUT /api/rooms/{id}/`
    *   **Body:** Full JSON object with all room details.
    *   **Note:** This will regenerate `dataenc`, the HMAC signature, and the QR code image for the updated room.
*   **Partially update a room:**
    *   `PATCH /api/rooms/{id}/`
    *   **Body:** JSON object with fields to update.
    *   **Note:** This will also regenerate `dataenc`, the HMAC signature, and the QR code image.
*   **Delete a room:**
    *   `DELETE /api/rooms/{id}/`
*   **Update Room Status (Custom Action):**
    *   `POST /api/rooms/{id}/update_status/`
    *   **Body:** JSON object `{ "status": "<new_status>" }` (e.g., `"active"`, `"inactive"`).

### 2. Departments

Manage department details.

*   **List all departments:**
    *   `GET /api/departments/`
*   **Create a new department:**
    *   `POST /api/departments/`
    *   **Body:** JSON object with department details (e.g., `dept_code`, `department_name`).
*   **Retrieve a single department:**
    *   `GET /api/departments/{dept_code}/`
*   **Update a department (full update):**
    *   `PUT /api/departments/{dept_code}/`
    *   **Body:** Full JSON object with all department details.
*   **Partially update a department:**
    *   `PATCH /api/departments/{dept_code}/`
    *   **Body:** JSON object with fields to update.
*   **Delete a department:**
    *   `DELETE /api/departments/{dept_code}/`

### 3. Issue Categories

Manage issue categories, linked to departments.

*   **List all issue categories:**
    *   `GET /api/issue-category/`
*   **Create a new issue category:**
    *   `POST /api/issue-category/`
    *   **Body:** JSON object with category details (e.g., `issue_category_code`, `department` (dept_code), `issue_category_name`).
*   **Retrieve a single issue category:**
    *   `GET /api/issue-category/{issue_category_code}/`
*   **Update an issue category (full update):**
    *   `PUT /api/issue-category/{issue_category_code}/`
    *   **Body:** Full JSON object with all category details.
*   **Partially update an issue category:**
    *   `PATCH /api/issue-category/{issue_category_code}/`
    *   **Body:** JSON object with fields to update.
*   **Delete an issue category:**
    *   `DELETE /api/issue-category/{issue_category_code}/`

### 4. Complaints

Manage complaint submissions, including image uploads and QR code data validation.

*   **List all complaints:**
    *   `GET /api/complaints/`
    *   **Query Parameters for filtering:** `status`, `priority`, `issue_type`, `ward`, `block`
    *   **Search Parameters:** `ticket_id`, `room_number`, `bed_number`, `description`
    *   **Ordering Parameters:** `submitted_at`, `priority`, `status`
*   **Create a new complaint:**
    *   `POST /api/complaints/`
    *   **Content-Type:** `multipart/form-data`
    *   **Body (Form Data):**
        *   All complaint fields (e.g., `bed_number`, `block`, `room_number`, `issue_type`, `description`, `priority`, etc.).
        *   `images`: (Optional) One or more image files.
        *   `qr_data_from_qr`: (Required if submitted via QR code scan) The `data` query parameter extracted from the QR code URL.
        *   `qr_signature_from_qr`: (Required if submitted via QR code scan) The `signature` query parameter extracted from the QR code URL.
    *   **HMAC Validation:** The backend validates `qr_data_from_qr` against `qr_signature_from_qr` using the `QR_CODE_SECRET_KEY` to prevent data tampering.
*   **Retrieve a single complaint:**
    *   `GET /api/complaints/{ticket_id}/`
    *   **Response includes:** Complaint details and URLs to associated `images`.
*   **Update a complaint (full update):**
    *   `PUT /api/complaints/{ticket_id}/`
    *   **Content-Type:** `multipart/form-data`
    *   **Body (Form Data):** Full set of complaint fields.
    *   **Note:** If `images` are included, they will be **appended** to the existing images.
*   **Partially update a complaint:**
    *   `PATCH /api/complaints/{ticket_id}/`
    *   **Content-Type:** `multipart/form-data`
    *   **Body (Form Data):** Fields to update.
    *   **Note:** If `images` are included, they will be **appended** to the existing images.
*   **Delete a complaint:**
    *   `DELETE /api/complaints/{ticket_id}/`
*   **Update Complaint Status (Custom Action):**
    *   `POST /api/complaints/{ticket_id}/update_status/`
    *   **Body:** JSON object `{ "status": "<new_status>", "remarks": "<optional_remarks>" }` (e.g., `"resolved"`, `"in_progress"`).
*   **Filter Complaints by Status (Custom Action):**
    *   `GET /api/complaints/by_status/`
    *   **Query Parameter:** `status=<status_value>` (e.g., `status=open`, `status=resolved`).
*   **Filter Complaints by Priority (Custom Action):**
    *   `GET /api/complaints/by_priority/`
    *   **Query Parameter:** `priority=<priority_value>` (e.g., `priority=low`, `priority=high`).

--- 