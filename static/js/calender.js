// JavaScript for the calendar interface

// Get the current date
var currentDate = new Date();

// Function to render the calendar
function renderCalendar(selectDateTime) {
  // Get the month and year
  var month = currentDate.getMonth();
  var year = currentDate.getFullYear();

  // Get the calendar container element
  var calendarContainer = document.getElementById('calendar');

  // Check if the calendar container exists
  if (!calendarContainer) {
    return;
  }

  // Clear the calendar container
  calendarContainer.innerHTML = '';

  // Create the month header
  var monthHeader = document.createElement('div');
  monthHeader.classList.add('month');
  monthHeader.textContent = monthName(month) + ' ' + year;
  calendarContainer.appendChild(monthHeader);

  // Create the days grid
  var daysGrid = document.createElement('div');
  daysGrid.classList.add('days');
  calendarContainer.appendChild(daysGrid);

  // Get the number of days in the current month
  var numDays = new Date(year, month + 1, 0).getDate();

  // Get the day of the week for the first day of the month
  var firstDay = new Date(year, month, 1).getDay();

  // Render the day cells
  for (var i = 0; i < firstDay; i++) {
    var emptyCell = document.createElement('div');
    daysGrid.appendChild(emptyCell);
  }

  for (var day = 1; day <= numDays; day++) {
    var dayCell = document.createElement('div');
    dayCell.classList.add('day');
    dayCell.textContent = day;
    daysGrid.appendChild(dayCell);

    // Add event listener to select the date
    dayCell.addEventListener('click', function () {
      selectDateTime(this.textContent);
    });
  }

  // Add active class to the current day
  var currentDayCell = daysGrid.querySelector('.day:nth-child(' + (currentDate.getDate() + firstDay) + ')');
  currentDayCell.classList.add('active');
}

// Function to get the month name
function monthName(monthIndex) {
  var months = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
  ];
  return months[monthIndex];
}

// Function to select the date
function selectDate(day) {
  // TODO: Handle the selected date
  console.log('Selected date: ' + day);
}

// Render the initial calendar
renderCalendar(selectDate); // Pass the selectDate function as a callback
