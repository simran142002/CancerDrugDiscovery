document.addEventListener('DOMContentLoaded', function() {
    fetchStudents();
});

function fetchStudents() {
    fetch('/api/students')
    .then(response => response.json())
    .then(data => {
        const studentList = document.getElementById('studentList');
        studentList.innerHTML = '';
        data.forEach(student => {
            const studentItem = document.createElement('div');
            studentItem.classList.add('student');
            studentItem.innerHTML = `
                <strong>Name:</strong> ${student.name}, 
                <strong>Age:</strong> ${student.age}, 
                <strong>Grade:</strong> ${student.grade}
            `;
            studentList.appendChild(studentItem);
        });
    })
    .catch(error => console.error('Error fetching students:', error));
}
