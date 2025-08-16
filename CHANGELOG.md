# CHANGELOG

## **[1.5.0]**
- Added comprehensive keyboard navigation support:
  - **Escape key:** Cancel/close datepicker
  - **Enter key:** Confirm selection
  - **D key:** Navigate to previous day (crosses month boundaries)
  - **A key:** Navigate to next day (crosses month boundaries)
  - **W key:** Navigate to previous week (stays within current month)
  - **S key:** Navigate to next week (stays within current month)
  - **Keyboard events only active in calendar mode (disabled in year/input modes)**
  - **Smart keyboard event isolation (only captures events when datepicker is open)**

## **[1.4.1]**
- **Added performance optimizations with LRU cache for faster date calculations**

## **[1.4]**
- **Added smart mode switching (input mode always returns to calendar mode)**
- **Added automatic input validation with Persian numeral support**
- **Added date memory control (reset to default vs. remember last selection)**
- **Added flexible show methods for different use cases**
- **Added today navigation button for quick date selection**
- **Added error handling with user-friendly Persian error messages**
- **Added comprehensive date range validation**
- **Added clean state management and mode isolation**

## **[1.3]**
- **Added input mode for direct date entry with validation**
- **Added animation for switching between input mode and calendar mode**

## **[1.2]**
- **Added button color change on mouse hover**
- **Added animation on clicking the year selection button**

## **[1.1]**
- **Added default date highlighting with yellow border**
- **Added last selected date visual distinction**

## **[1.0]**
- **Initial release with Persian calendar and proper Shamsi dates**
- **Month and year navigation**
- **Floating overlay display**
- **RTL (Right-to-Left) support**
- **Persian numerals and month names**
- **Callback system for date selection**