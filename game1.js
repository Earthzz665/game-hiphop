const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let player = {
    x: canvas.width / 2 - 20,
    y: canvas.height - 50,
    width: 40,
    height: 40,
    speed: 7,
    dx: 0
};

let objects = [];
let objectSpeed = 5;
let score = 0;
let gameOver = false;

// สร้างวัตถุที่ตกลงมา
function createObject() {
    const size = Math.random() * 30 + 20;
    const x = Math.random() * (canvas.width - size);
    objects.push({ x: x, y: 0, width: size, height: size });
}

// วาดผู้เล่น
function drawPlayer() {
    ctx.fillStyle = 'blue';
    ctx.fillRect(player.x, player.y, player.width, player.height);
}

// วาดวัตถุที่ตกลงมา
function drawObjects() {
    ctx.fillStyle = 'red';
    objects.forEach(object => {
        ctx.fillRect(object.x, object.y, object.width, object.height);
    });
}

// อัปเดตการเคลื่อนไหวของผู้เล่น
function movePlayer() {
    player.x += player.dx;

    if (player.x < 0) {
        player.x = 0;
    } else if (player.x + player.width > canvas.width) {
        player.x = canvas.width - player.width;
    }
}

// อัปเดตการเคลื่อนไหวของวัตถุ
function moveObjects() {
    objects.forEach((object, index) => {
        object.y += objectSpeed;

        // ลบวัตถุที่ตกถึงขอบล่างของจอ
        if (object.y > canvas.height) {
            objects.splice(index, 1);
            score++;
            document.getElementById('score').innerText = `Score: ${score}`;
        }

        // ตรวจสอบการชนของผู้เล่นกับวัตถุ
        if (object.y < player.y + player.height &&
            object.y + object.height > player.y &&
            object.x < player.x + player.width &&
            object.x + object.width > player.x) {
            gameOver = true;
        }
    });
}

// เคลียร์ Canvas
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// อัปเดตเฟรมของเกม
function update() {
    if (!gameOver) {
        clearCanvas();
        drawPlayer();
        drawObjects();
        movePlayer();
        moveObjects();

        requestAnimationFrame(update);
    } else {
        alert('Game Over! Your score: ' + score);
        window.location.reload();
    }
}

// เริ่มเกม
function startGame() {
    setInterval(createObject, 1000);
    update();
}

// ควบคุมผู้เล่นด้วยปุ่มลูกศร
function moveRight() {
    player.dx = player.speed;
}

function moveLeft() {
    player.dx = -player.speed;
}

function stopMove() {
    player.dx = 0;
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
        moveRight();
    } else if (e.key === 'ArrowLeft') {
        moveLeft();
    }
});

document.addEventListener('keyup', stopMove);

// เริ่มเกมทันทีที่โหลด
startGame();
