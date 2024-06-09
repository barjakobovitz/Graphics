import * as THREE from 'three';
import {OrbitControls} from './OrbitControls.js'


const WHITE_COLOR = 0xffffff;
const BLACK_COLOR = 0x000000;
const LIGHT_GRAY_COLOR = 0xd3d3d3;
const GOAL_HEIGHT = 2;
let scale = 1;
let isWireframe = false;


const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );
scene.background = new THREE.Color( 'ForestGreen' );

function degrees_to_radians(degrees)
{
  var pi = Math.PI;
  return degrees * (pi/180);
}

// LIGHTS

const hemiLight = new THREE.HemisphereLight( 0xffffff, 0xffffff, 2 );
hemiLight.color.setHSL( 0.6, 1, 0.6 );
hemiLight.groundColor.setHSL( 0.095, 1, 0.75 );
hemiLight.position.set( 0, 50, 0 );
scene.add( hemiLight );


const dirLight = new THREE.DirectionalLight( 0xffffff, 3 );
dirLight.color.setHSL( 0.1, 1, 0.95 );
dirLight.position.set( - 1, 1.75, 1 );
dirLight.position.multiplyScalar( 30 );
scene.add( dirLight );

dirLight.castShadow = true;

dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;

const d = 50;

dirLight.shadow.camera.left = - d;
dirLight.shadow.camera.right = d;
dirLight.shadow.camera.top = d;
dirLight.shadow.camera.bottom = - d;

dirLight.shadow.camera.far = 3500;
dirLight.shadow.bias = - 0.0001;


// Add here the rendering of your goal

// Ball
const ballGeometry = new THREE.SphereGeometry(GOAL_HEIGHT * scale / 8, 32, 32);
const ballMaterial = new THREE.MeshPhongMaterial({color: BLACK_COLOR, wireframe: isWireframe});
const ball = new THREE.Mesh(ballGeometry, ballMaterial);
scene.add(ball);

// GOAL
const goalMaterial = new THREE.MeshPhongMaterial( {color: WHITE_COLOR} ); // white

// Goal crossbar
const crossBarLength = 3 * GOAL_HEIGHT * scale;
const goalCrossBarGeometry = new THREE.CylinderGeometry(0.1,0.1, crossBarLength,32);
const goalCrossBar = new THREE.Mesh(goalCrossBarGeometry, goalMaterial);
const goalCrossBarPositionMatrix = new THREE.Matrix4().makeTranslation(0, GOAL_HEIGHT / 2, -2);
const crossBarRotateMatrix = new THREE.Matrix4().makeRotationZ(Math.PI / 2);
const crossBarTranslateMatrix = new THREE.Matrix4().multiplyMatrices(goalCrossBarPositionMatrix, crossBarRotateMatrix);
goalCrossBar.applyMatrix4(crossBarTranslateMatrix);

// Goal posts
const goalPostGeometry = new THREE.CylinderGeometry(0.105,0.105, GOAL_HEIGHT + 0.1,32);
const goalRightPost = new THREE.Mesh(goalPostGeometry, goalMaterial);
const goalLeftPost = new THREE.Mesh(goalPostGeometry, goalMaterial);
const postPosition = (GOAL_HEIGHT * 3) / 2 - 0.1;
const goalRightPostTranslateMatrix = new THREE.Matrix4().makeTranslation(postPosition + 0.0675,0.05,-2);
const goalLeftPostTranslateMatrix = new THREE.Matrix4().makeTranslation(-postPosition - 0.0675,0.05,-2);
goalRightPost.applyMatrix4(goalRightPostTranslateMatrix);
goalLeftPost.applyMatrix4(goalLeftPostTranslateMatrix);

// Goal post supports
const goalSupportAngle = 45;
const goalPostSupportLength = GOAL_HEIGHT / Math.cos(degrees_to_radians(goalSupportAngle)) + 0.1;
const goalPostSupportGeometry = new THREE.CylinderGeometry(0.05,0.05, goalPostSupportLength,32);
const goalRightPostSupport = new THREE.Mesh(goalPostSupportGeometry, goalMaterial);
const goalLeftPostSupport = new THREE.Mesh(goalPostSupportGeometry, goalMaterial);
const postSupportRotationMatrix = new THREE.Matrix4();
postSupportRotationMatrix.makeRotationX(degrees_to_radians(goalSupportAngle));
const goalLeftPostSupportTranslateMatrix = new THREE.Matrix4().makeTranslation(-postPosition - 0.066,0, (-postPosition / 3) - 2.025).multiply(postSupportRotationMatrix);
const goalRightPostSupportTranslateMatrix = new THREE.Matrix4().makeTranslation(postPosition + 0.066,0,(-postPosition / 3) - 2.025).multiply(postSupportRotationMatrix);
goalRightPostSupport.applyMatrix4(goalRightPostSupportTranslateMatrix);
goalLeftPostSupport.applyMatrix4(goalLeftPostSupportTranslateMatrix);

// Goal post torus
const goalTorusMaterial = new THREE.MeshPhongMaterial( {color: 0xffffff, side: THREE.DoubleSide, wireframe:isWireframe} );
const goalTorusGeometry = new THREE.RingGeometry(0,0.2,32);
const goalRightPostTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const goalRightPostSupportTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const goalLeftPostTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const goalLeftPostSupportTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const supportTorusPosition = GOAL_HEIGHT / Math.tan(degrees_to_radians(goalSupportAngle)) - 0.1;
const torusRotationMatrix = new THREE.Matrix4();
torusRotationMatrix.makeRotationX(degrees_to_radians(90));
const goalLeftPostTorusTranslateMatrix = new THREE.Matrix4().makeTranslation(-postPosition - 0.0675,-GOAL_HEIGHT / 2,-2).multiply(torusRotationMatrix);
const goalLeftPostSupportTorusTranslateMatrix = new THREE.Matrix4().makeTranslation(-postPosition - 0.066, -GOAL_HEIGHT / 2,  -supportTorusPosition - 2.125).multiply(torusRotationMatrix);
const goalRightPostSupportTorusTranslateMatrix = new THREE.Matrix4().makeTranslation(postPosition + 0.066, -GOAL_HEIGHT / 2,  -supportTorusPosition - 2.125).multiply(torusRotationMatrix);
const goalRightPostTorusTranslateMatrix = new THREE.Matrix4().makeTranslation(postPosition + 0.0675, -GOAL_HEIGHT / 2, -2).multiply(torusRotationMatrix);
goalRightPostTorus.applyMatrix4(goalRightPostTorusTranslateMatrix);
goalLeftPostTorus.applyMatrix4(goalLeftPostTorusTranslateMatrix);
goalRightPostSupportTorus.applyMatrix4(goalRightPostSupportTorusTranslateMatrix);
goalLeftPostSupportTorus.applyMatrix4(goalLeftPostSupportTorusTranslateMatrix);


// Goal net
const goalNetMaterial = new THREE.MeshPhongMaterial({
	color: LIGHT_GRAY_COLOR,
	side: THREE.DoubleSide,
	wireframe: isWireframe
});

// Main net behind the goal
const goalNetGeometry = new THREE.PlaneGeometry(crossBarLength, goalPostSupportLength - 0.1, 32);
const goalNet = new THREE.Mesh(goalNetGeometry, goalNetMaterial);
const goalNetRotationMatrix = new THREE.Matrix4().makeRotationX(Math.PI / 4);
const goalNetPositionMatrix = new THREE.Matrix4().makeTranslation(0, 0, (-postPosition / 3) - 2.025);
const goalNetTranslateMatrix = new THREE.Matrix4().multiplyMatrices(goalNetPositionMatrix, goalNetRotationMatrix);
goalNet.applyMatrix4(goalNetTranslateMatrix);

// Side nets
const sideNetHeight = GOAL_HEIGHT;
const sideNetGeometry = new THREE.BufferGeometry();
const vertices = new Float32Array([
	0, 0, 0, // bottom vertex at the base of the post
	0, sideNetHeight, 0, // top vertex at the top of the post
	(15/24) * GOAL_HEIGHT * Math.tan(goalSupportAngle), 0, 0 // bottom vertex at the end of the support
]);
sideNetGeometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
sideNetGeometry.setIndex([0, 1, 2]); // Defining the face using the vertices
sideNetGeometry.computeVertexNormals();

// Left side net
const leftSideNet = new THREE.Mesh(sideNetGeometry, goalNetMaterial);
leftSideNet.position.set(-1.5 * GOAL_HEIGHT, (-sideNetHeight / 2), -2); // Positioning left net
leftSideNet.rotation.y = Math.PI / 2; // Rotate to face towards the goal

// Right side net
const rightSideNet = new THREE.Mesh(sideNetGeometry, goalNetMaterial);
rightSideNet.position.set(1.5 * GOAL_HEIGHT, (-sideNetHeight / 2), -2); // Positioning left net
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



// This defines the initial distance of the camera
const cameraTranslate = new THREE.Matrix4();
cameraTranslate.makeTranslation(0,0,5);
camera.applyMatrix4(cameraTranslate)

renderer.render( scene, camera );

const controls = new OrbitControls( camera, renderer.domElement );

let isOrbitEnabled = true;

const toggleOrbit = (e) => {
	if (e.key === "o"){
		isOrbitEnabled = !isOrbitEnabled;
	}
}

const toggleWireframe = (e) => {
	if (e.key === "w"){
		isWireframe = !isWireframe;
		ballMaterial.wireframe = isWireframe;
		goalMaterial.wireframe = isWireframe;
		goalNetMaterial.wireframe = isWireframe;
		goalTorusMaterial.wireframe = isWireframe;
	}
}


document.addEventListener('keydown',toggleOrbit)
document.addEventListener('keydown',toggleWireframe)

//controls.update() must be called after any manual changes to the camera's transform
controls.update();

function animate() {

	requestAnimationFrame( animate );

	controls.enabled = isOrbitEnabled;
	controls.update();

	renderer.render( scene, camera );

}
animate()