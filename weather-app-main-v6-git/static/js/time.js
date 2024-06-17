function displayCurrentDateTime() {
    const now = new Date();

    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const dayOfWeek = daysOfWeek[now.getDay()];

    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const month = months[now.getMonth()];

    const date = now.getDate().toString().padStart(2, '0');
    const year = now.getFullYear();

    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');

    const dateTimeString = `${dayOfWeek}, ${month} ${date}, ${year} ${hours}:${minutes}:${seconds}`;
    document.getElementById('currentDateTime').textContent = dateTimeString;
}

//Call the function initially
displayCurrentDateTime();

//Update the date and time every second
setInterval(displayCurrentDateTime, 1000);