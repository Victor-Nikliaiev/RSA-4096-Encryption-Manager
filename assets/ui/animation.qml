import QtQuick 2.15
import QtQuick.Controls 2.15

 
Rectangle {
    color: "#263238"

    Image {
        id: animatedImage
        source: "icons/binary-code.png"  // Replace with the path to your image
        anchors.centerIn: parent

        // Define custom properties for original size
        property real originalWidth: 120
        property real originalHeight: 120
        property real animationTime: 100

        // Initialize width and height using custom properties
        width: originalWidth
        height: originalHeight

        // Animation for scaling width
        SequentialAnimation on width {
            loops: Animation.Infinite  // Endless loop
            NumberAnimation {
                to: animatedImage.originalWidth * 1.02  // Scale to 150%
                duration: animatedImage.animationTime                       // Duration to grow (1 second)
                easing.type: Easing.InOutQuad
            }
            NumberAnimation {
                to: animatedImage.originalWidth  // Back to original size
                duration: animatedImage.animationTime                   // Duration to shrink (1 second)
                easing.type: Easing.InOutQuad
            }
        }

         SequentialAnimation on height {
            loops: Animation.Infinite  // Endless loop
            NumberAnimation {
                to: animatedImage.originalHeight * 1.02  // Scale to 150%
                duration: animatedImage.animationTime                        // Duration to grow (1 second)
                easing.type: Easing.InOutQuad
            }
            NumberAnimation {
                to: animatedImage.originalHeight  // Back to original size
                duration: animatedImage.animationTime                   // Duration to shrink (1 second)
                easing.type: Easing.InOutQuad
            }
        }
    }
}
    
 
