import * as THREE from 'three';
import {OrbitControls} from './OrbitControls.js'

let goalHeight = 2;

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

// Add here the rendering of your goal

// Ball
const ballGeometry = new THREE.SphereGeometry(goalHeight / 8, 32, 32);
const ballMaterial = new THREE.MeshBasicMaterial({color: 0x000000});
const ball = new THREE.Mesh(ballGeometry, ballMaterial);
scene.add(ball);

// GOAL
const goalMaterial = new THREE.MeshBasicMaterial( {color: 0xffffff} ); // white
// Goal crossbar
const crossBarLength = 3 * goalHeight;
const goalCrossBarGeometry = new THREE.CylinderGeometry(0.1,0.1, crossBarLength,32);
const goalCrossBar = new THREE.Mesh(goalCrossBarGeometry, goalMaterial);
const crossBarPosition = goalHeight / 2;
const goalCrossBarRotationMatrix = new THREE.Matrix4();
const crossBarTranslateMatrix = new THREE.Matrix4();

goalCrossBarRotationMatrix.makeRotationZ(degrees_to_radians(90));
goalCrossBar.applyMatrix4(goalCrossBarRotationMatrix);
crossBarTranslateMatrix.makeTranslation(0,crossBarPosition, 0);
goalCrossBar.applyMatrix4(crossBarTranslateMatrix);

// Goal posts
const goalPostGeometry = new THREE.CylinderGeometry(0.1,0.1, goalHeight,32);
const goalRightPost = new THREE.Mesh(goalPostGeometry, goalMaterial);
const goalLeftPost = new THREE.Mesh(goalPostGeometry, goalMaterial);
const postPosition = (goalHeight * 3) / 2 - 0.1;
const movePositionMatrix = new THREE.Matrix4();

movePositionMatrix.makeTranslation(postPosition ,0,0);
goalRightPost.applyMatrix4(movePositionMatrix);
movePositionMatrix.makeTranslation(-postPosition ,0,0);
goalLeftPost.applyMatrix4(movePositionMatrix);

// Goal post supports
const goalSupportAngle = 45;
const goalPostSupportLength = goalHeight / Math.cos(degrees_to_radians(goalSupportAngle));
const goalPostSupportGeometry = new THREE.CylinderGeometry(0.1,0.1, goalPostSupportLength,32);
const goalRightPostSupport = new THREE.Mesh(goalPostSupportGeometry, goalMaterial);
const goalLeftPostSupport = new THREE.Mesh(goalPostSupportGeometry, goalMaterial);
const postSupportTranslateMatrix = new THREE.Matrix4();
const postSupportRotationMatrix = new THREE.Matrix4();

postSupportRotationMatrix.makeRotationX(degrees_to_radians(goalSupportAngle));
goalRightPostSupport.applyMatrix4(postSupportRotationMatrix);
goalLeftPostSupport.applyMatrix4(postSupportRotationMatrix);
postSupportTranslateMatrix.makeTranslation(postPosition,0,-postPosition / 3);
goalRightPostSupport.applyMatrix4(postSupportTranslateMatrix);
postSupportTranslateMatrix.makeTranslation(-postPosition,0,-postPosition / 3);
goalLeftPostSupport.applyMatrix4(postSupportTranslateMatrix);

// Goal post torus
const goalTorusMaterial = new THREE.MeshBasicMaterial( {color: 0xffffff, side: THREE.DoubleSide} );
const goalTorusGeometry = new THREE.RingGeometry(0,0.2,32);
const goalRightPostTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const goalRightPostSupportTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const goalLeftPostTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const goalLeftPostSupportTorus = new THREE.Mesh(goalTorusGeometry, goalTorusMaterial);
const torusTranslateMatrix = new THREE.Matrix4();
const torusRotationMatrix = new THREE.Matrix4();
const supportTorusPosition = goalHeight / Math.tan(degrees_to_radians(goalSupportAngle)) - 0.1;

torusRotationMatrix.makeRotationX(degrees_to_radians(90));
torusTranslateMatrix.makeTranslation(postPosition,-goalHeight / 2,0);
goalRightPostTorus.applyMatrix4(torusRotationMatrix);
goalRightPostTorus.applyMatrix4(torusTranslateMatrix);
torusTranslateMatrix.makeTranslation(-postPosition,-goalHeight / 2,0);
goalLeftPostTorus.applyMatrix4(torusRotationMatrix);
goalLeftPostTorus.applyMatrix4(torusTranslateMatrix);
torusTranslateMatrix.makeTranslation(postPosition,-goalHeight / 2, -supportTorusPosition);
goalRightPostSupportTorus.applyMatrix4(torusRotationMatrix);
goalRightPostSupportTorus.applyMatrix4(torusTranslateMatrix);
torusTranslateMatrix.makeTranslation(-postPosition,-goalHeight / 2, -supportTorusPosition);
goalLeftPostSupportTorus.applyMatrix4(torusRotationMatrix);
goalLeftPostSupportTorus.applyMatrix4(torusTranslateMatrix);

// Goal net
const goalNetMaterial = new THREE.MeshBasicMaterial({color: 0xdddddd, side: THREE.DoubleSide});
const goalNetGeometry = new THREE.PlaneGeometry(goalHeight * 3, goalHeight * 1.45, 32);
const goalNet = new THREE.Mesh(goalNetGeometry, goalNetMaterial);
const goalNetPositionMatrix = new THREE.Matrix4();
const goalNetRotationMatrix = new THREE.Matrix4();
goalNetPositionMatrix.makeTranslation(0,-goalHeight / 2.75,-goalHeight / 2.6);
goalNetRotationMatrix.makeRotationX(degrees_to_radians(goalSupportAngle));
goalNet.applyMatrix4(goalNetPositionMatrix);
goalNet.applyMatrix4(goalNetRotationMatrix);

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



// This defines the initial distance of the camera
const cameraTranslate = new THREE.Matrix4();
cameraTranslate.makeTranslation(0,0,5);
camera.applyMatrix4(cameraTranslate)

renderer.render( scene, camera );

const controls = new OrbitControls( camera, renderer.domElement );

let isOrbitEnabled = true;

const toggleOrbit = (e) => {
	if (e.key == "o"){
		isOrbitEnabled = !isOrbitEnabled;
	}
}

document.addEventListener('keydown',toggleOrbit)

//controls.update() must be called after any manual changes to the camera's transform
controls.update();

function animate() {

	requestAnimationFrame( animate );

	controls.enabled = isOrbitEnabled;
	controls.update();

	renderer.render( scene, camera );

}
animate()