import QtQuick 1.0
 
Rectangle {
 
    id: main
    width: 200
    height: 300
    anchors.fill: parent
    color: "#343434"
   
 
    ListModel {
        id: model
 
        ListElement {
            value: 1
        }
 
        ListElement {
            value: 2
        }
 
        ListElement {
            value: 3
        }
 
        ListElement {
            value: 4
        }
 
        ListElement {
            value: 5
        }
    }
 
    Rectangle {
        id: comboBoxContainer            
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.leftMargin: parent.width/4
        anchors.topMargin: parent.height/6
        width: parent.width/2
        height: parent.height/6
        color: "#343434"
        z: 1
   
        ComboBox {
            id: comboBox            
            anchors.top: parent.top
            anchors.left: parent.left
            width: main.width/2
            height: main.height/6
            initialText: "1"
            maxHeight: main.height/2
            listModel: model
 
            onExpanded: {
                comboBoxContainer.height = main.height/3*2
            }    
 
            onClosed: {
                comboBoxContainer.height = main.height/6
            }    
        }        
    }
   
    Text {
        id: gamePriceText
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.leftMargin: parent.width/4
        anchors.bottomMargin: parent.height/6
        width: parent.width/2
        height: parent.height/6        
        color: "#fff"
        text: "Some text"
        font.pixelSize: 20
        font.bold: true      
    }
}