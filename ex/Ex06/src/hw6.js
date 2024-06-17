const WHITE_COLOR = 0xffffff;
const BLACK_COLOR = 0x000000;
const LIGHT_GRAY_COLOR = 0xd3d3d3;
const GOAL_HEIGHT = 16;
const GOAL_Z_POSITION = -50;


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
const ball_texture = textureLoader.load('src/textures/soccer_ball.jpg');
const red_card_texture = textureLoader.load('src/textures/red_card.jpg');
const yellow_card_texture = textureLoader.load('src/textures/yellow_card.jpg');
const net_texture = textureLoader.load('src/textures/goal_net.png');



// TODO: Add Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);  // soft white light
scene.add(ambientLight);

// Directional Light 1 - from one end of the field
const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight1.position.set(0, 0, 0);  // Adjust position based on the scene setup
directionalLight1.castShadow = true;
scene.add(directionalLight1);

// Directional Light 2 - from the opposite end
const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight2.position.set(0, 0, 100);  // Adjust position based on the scene setup
directionalLight2.castShadow = true;
scene.add(directionalLight2);

renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// TODO: Goal
// You should copy-paste the goal from the previous exercise here
const goalMaterial = new THREE.MeshPhongMaterial( {color: WHITE_COLOR} ); // white
// Goal crossbar
const crossBarLength = 3 * GOAL_HEIGHT + 1;
const goalCrossBarGeometry = new THREE.CylinderGeometry(1,1, crossBarLength,32);
const goalCrossBar = new THREE.Mesh(goalCrossBarGeometry, goalMaterial);
const goalCrossBarPositionMatrix = new THREE.Matrix4().makeTranslation(0, GOAL_HEIGHT / 2, GOAL_Z_POSITION);
const crossBarRotateMatrix = new THREE.Matrix4().makeRotationZ(Math.PI / 2);
const crossBarTranslateMatrix = new THREE.Matrix4().multiplyMatrices(goalCrossBarPositionMatrix, crossBarRotateMatrix);
goalCrossBar.applyMatrix4(crossBarTranslateMatrix);

// Goal posts
const goalPostGeometry = new THREE.CylinderGeometry(0.75,0.75, GOAL_HEIGHT + 0.75,32);
const goalRightPost = new THREE.Mesh(goalPostGeometry, goalMaterial);
const goalLeftPost = new THREE.Mesh(goalPostGeometry, goalMaterial);
const postPosition = (GOAL_HEIGHT * 3) / 2 - 0.1;
const goalRightPostTranslateMatrix = new THREE.Matrix4().makeTranslation(postPosition + 0.0675,0.05, GOAL_Z_POSITION);
const goalLeftPostTranslateMatrix = new THREE.Matrix4().makeTranslation(-postPosition - 0.0675,0.05, GOAL_Z_POSITION);
goalRightPost.applyMatrix4(goalRightPostTranslateMatrix);
goalLeftPost.applyMatrix4(goalLeftPostTranslateMatrix);

// Goal post supports
const goalSupportAngle = 45;
const goalPostSupportLength = GOAL_HEIGHT / Math.cos(degrees_to_radians(goalSupportAngle)) + 1;
const goalPostSupportGeometry = new THREE.CylinderGeometry(0.5,0.5, goalPostSupportLength,32);
const goalRightPostSupport = new THREE.Mesh(goalPostSupportGeometry, goalMaterial);
const goalLeftPostSupport = new THREE.Mesh(goalPostSupportGeometry, goalMaterial);
const postSupportRotationMatrix = new THREE.Matrix4();
postSupportRotationMatrix.makeRotationX(degrees_to_radians(goalSupportAngle));
const goalLeftPostSupportTranslateMatrix = new THREE.Matrix4().makeTranslation(-postPosition,0, (-postPosition / 3) + (GOAL_Z_POSITION - 0.025)).multiply(postSupportRotationMatrix);
const goalRightPostSupportTranslateMatrix = new THREE.Matrix4().makeTranslation(postPosition    ,0,(-postPosition / 3) + (GOAL_Z_POSITION - 0.025)).multiply(postSupportRotationMatrix);
goalRightPostSupport.applyMatrix4(goalRightPostSupportTranslateMatrix);
goalLeftPostSupport.applyMatrix4(goalLeftPostSupportTranslateMatrix);

// Goal post torus
const goalTorusMaterial = new THREE.MeshPhongMaterial( {color: WHITE_COLOR, side: THREE.DoubleSide} );
const goalTorusGeometry = new THREE.RingGeometry(0,1.25,32);
const goalSupportTorusGeometry = new THREE.RingGeometry(0,1,32);
const goalRightPostTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const goalRightPostSupportTorus = new THREE.Mesh(goalSupportTorusGeometry, goalTorusMaterial);
const goalLeftPostTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const goalLeftPostSupportTorus = new THREE.Mesh(goalSupportTorusGeometry, goalTorusMaterial);
const supportTorusPosition = GOAL_HEIGHT / Math.tan(degrees_to_radians(goalSupportAngle)) - 0.1;
const torusRotationMatrix = new THREE.Matrix4();
torusRotationMatrix.makeRotationX(degrees_to_radians(90));
const goalLeftPostTorusTranslateMatrix = new THREE.Matrix4().makeTranslation(-postPosition,-GOAL_HEIGHT / 2 - 0.25, GOAL_Z_POSITION).multiply(torusRotationMatrix);
const goalLeftPostSupportTorusTranslateMatrix = new THREE.Matrix4().makeTranslation(-postPosition, -GOAL_HEIGHT / 2 - 0.3,  -supportTorusPosition + (GOAL_Z_POSITION - 0.1)).multiply(torusRotationMatrix);
const goalRightPostSupportTorusTranslateMatrix = new THREE.Matrix4().makeTranslation(postPosition, -GOAL_HEIGHT / 2 - 0.3,  -supportTorusPosition + (GOAL_Z_POSITION - 0.1)).multiply(torusRotationMatrix);
const goalRightPostTorusTranslateMatrix = new THREE.Matrix4().makeTranslation(postPosition, -GOAL_HEIGHT / 2 - 0.25, GOAL_Z_POSITION).multiply(torusRotationMatrix);
goalRightPostTorus.applyMatrix4(goalRightPostTorusTranslateMatrix);
goalLeftPostTorus.applyMatrix4(goalLeftPostTorusTranslateMatrix);
goalRightPostSupportTorus.applyMatrix4(goalRightPostSupportTorusTranslateMatrix);
goalLeftPostSupportTorus.applyMatrix4(goalLeftPostSupportTorusTranslateMatrix);

// Goal net
const goalNetMaterial = new THREE.MeshPhongMaterial({
    map: net_texture,
    color: LIGHT_GRAY_COLOR,
    side: THREE.DoubleSide,
    opacity: 0.8,
    transparent: true
});

// Main net behind the goal
const goalNetGeometry = new THREE.PlaneGeometry(crossBarLength, goalPostSupportLength - 0.1, 32);
const goalNet = new THREE.Mesh(goalNetGeometry, goalNetMaterial);
const goalNetRotationMatrix = new THREE.Matrix4().makeRotationX(Math.PI / 4);
const goalNetPositionMatrix = new THREE.Matrix4().makeTranslation(0, 0, (-postPosition / 3) + (GOAL_Z_POSITION - 0.025));
const goalNetTranslateMatrix = new THREE.Matrix4().multiplyMatrices(goalNetPositionMatrix, goalNetRotationMatrix);
goalNet.applyMatrix4(goalNetTranslateMatrix);

// Side nets
const sideNetHeight = GOAL_HEIGHT;
const sideNetGeometry = new THREE.BufferGeometry();
const vertices = new Float32Array([
    0, 0, 0, // bottom vertex at the base of the post
    0, sideNetHeight + 0.5, 0, // top vertex at the top of the post
    (15/24) * GOAL_HEIGHT * Math.tan(goalSupportAngle), 0, 0 // bottom vertex at the end of the support
]);
sideNetGeometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
sideNetGeometry.setIndex([0, 1, 2]); // Defining the face using the vertices

// Define UV coordinates for the triangle
const uvs = new Float32Array([
    0, 0, // UV for the bottom vertex at the base of the post
    0, 1, // UV for the top vertex at the top of the post
    1, 0  // UV for the bottom vertex at the end of the support
]);
sideNetGeometry.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));

sideNetGeometry.computeVertexNormals();
sideNetGeometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
sideNetGeometry.setIndex([0, 1, 2]); // Defining the face using the vertices
sideNetGeometry.computeVertexNormals();

// Left side net
const leftSideNet = new THREE.Mesh(sideNetGeometry, goalNetMaterial);
leftSideNet.position.set(-1.5 * GOAL_HEIGHT, (-sideNetHeight / 2), GOAL_Z_POSITION); // Positioning left net
leftSideNet.rotation.y = Math.PI / 2; // Rotate to face towards the goal

// Right side net
const rightSideNet = new THREE.Mesh(sideNetGeometry, goalNetMaterial);
rightSideNet.position.set(1.5 * GOAL_HEIGHT, (-sideNetHeight / 2), GOAL_Z_POSITION); // Positioning left net
rightSideNet.rotation.y = Math.PI / 2; // Rotate to face towards the goal
scene.add(goalCrossBar);
scene.add(goalRightPost);
scene.add(goalLeftPost);
scene.add(goalRightPostSupport);
scene.add(goalLeftPostSupport);
scene.add(goalRightPostSupportTorus);
scene.add(goalLeftPostSupportTorus);
scene.add(goalLeftPostTorus);
scene.add(goalRightPostTorus);
scene.add(goalNet);
scene.add(leftSideNet);
scene.add(rightSideNet);


// TODO: Ball
// You should add the ball with the soccer.jpg texture here
const ballGeometry = new THREE.SphereGeometry(GOAL_HEIGHT / 16, 32, 32);
const ballMaterial = new THREE.MeshPhongMaterial({
    map: ball_texture,
    color: LIGHT_GRAY_COLOR,
    side: THREE.DoubleSide,
});
const ball = new THREE.Mesh(ballGeometry, ballMaterial);
const ballPositionMatrix = new THREE.Matrix4().makeTranslation(0, 0, 100);
ball.applyMatrix4(ballPositionMatrix)
scene.add(ball);

// TODO: Bezier Curves


// TODO: Camera Settings
// Set the camera following the ball here


// TODO: Add collectible cards with textures





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