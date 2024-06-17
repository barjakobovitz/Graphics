// Scene Declartion
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
// This defines the initial distance of the camera, you may ignore this as the camera is expected to be dynamic
camera.applyMatrix4(new THREE.Matrix4().makeTranslation(-5, 3, 110));
camera.lookAt(0, -4, 1)


const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );


// helper function for later on
function degrees_to_radians(degrees)
{
  var pi = Math.PI;
  return degrees * (pi/180);
}


// Here we load the cubemap and pitch images, you may change it

const loader = new THREE.CubeTextureLoader();
const texture = loader.load([
  'src/pitch/right.jpg',
  'src/pitch/left.jpg',
  'src/pitch/top.jpg',
  'src/pitch/bottom.jpg',
  'src/pitch/front.jpg',
  'src/pitch/back.jpg',
]);
scene.background = texture;


// TODO: Texture Loading
// We usually do the texture loading before we start everything else, as it might take processing time
const textureLoader = new THREE.TextureLoader();
const yellowCardTexture = textureLoader.load('src/textures/yellow_card.jpg');
const redCardTexture = textureLoader.load('src/textures/red_card.jpg');



// TODO: Add Lighting



// TODO: Goal
// You should copy-paste the goal from the previous exercise here


// TODO: Ball
// You should add the ball with the soccer.jpg texture here


// TODO: Bezier Curves
const start = new THREE.Vector3(0, 0, 100);
const end = new THREE.Vector3(0, 0, 0);

const controlRightWinger = new THREE.Vector3(50, 0, 50);
const controlCenterForward = new THREE.Vector3(0, 50, 50);
const controlLeftWinger = new THREE.Vector3(-50, 0, 50);

const curveRightWinger = new THREE.QuadraticBezierCurve3(start, controlRightWinger, end);
const curveCenterForward = new THREE.QuadraticBezierCurve3(start, controlCenterForward, end);
const curveLeftWinger = new THREE.QuadraticBezierCurve3(start, controlLeftWinger, end);

function drawCurve(curve, color) {
    const points = curve.getPoints(50);
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ color: color });
    const curveObject = new THREE.Line(geometry, material);
    scene.add(curveObject);
}

drawCurve(curveRightWinger, 0xff0000); // Red for right winger
drawCurve(curveCenterForward, 0x00ff00); // Green for center forward
drawCurve(curveLeftWinger, 0x0000ff); // Blue for left winger


// TODO: Camera Settings
// Set the camera following the ball here


// TODO: Add collectible cards with textures
const cardGeometry = new THREE.PlaneGeometry(1, 1.5);
const positions = [80, 60, 40, 20, 10, 0];
class Card {
    constructor(curve, t, object3D) {
        this.curve = curve;
        this.t = t;
        this.object3D = object3D;
    }
}

// Define the list to hold all cards
const cards = [];

// Function to create and place a card on a curve
function createCardOnCurve(curve, t, texture) {
    const cardGeometry = new THREE.PlaneGeometry(1, 1.5);  // Standard card size
    const cardMaterial = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide });
    const cardMesh = new THREE.Mesh(cardGeometry, cardMaterial);
    cardMesh.position.copy(curve.getPointAt(t));
    cardMesh.lookAt(new THREE.Vector3());  // Make the card face the origin or adjust as necessary
    scene.add(cardMesh);
    return new Card(curve, t, cardMesh);
}

// Function to initialize cards with random distribution
function initializeCards() {
    const curves = [curveRightWinger, curveCenterForward, curveLeftWinger];
    curves.forEach(curve => {
        const numCards = Math.floor(Math.random() * 3) + 2;  // Random number of cards between 2 and 4
        let hasYellow = false;
        let hasRed = false;

        for (let i = 0; i < numCards; i++) {
            let t = Math.random();  // Random t value along the curve
            let texture;
            if ((i === numCards - 1 && !hasYellow) || Math.random() > 0.5) {
                texture = yellowCardTexture;
                hasYellow = true;
            } else {
                texture = redCardTexture;
                hasRed = true;
            }
            cards.push(createCardOnCurve(curve, t, texture));
        }
    });

    // Sort cards by t value (optional, depends on use-case)
    cards.sort((a, b) => a.t - b.t);
}

// Call initializeCards at the appropriate time in your code
initializeCards();




// TODO: Add keyboard event
// We wrote some of the function for you
const handle_keydown = (e) => {
	if(e.code == 'ArrowLeft'){
		// TODO
	} else if (e.code == 'ArrowRight'){
		// TODO
	}
}
document.addEventListener('keydown', handle_keydown);



function animate() {

	requestAnimationFrame( animate );

	// TODO: Animation for the ball's position


	// TODO: Test for card-ball collision

	
	renderer.render( scene, camera );

}
animate()