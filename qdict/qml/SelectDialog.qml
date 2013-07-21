import QtQuick 1.0

SelectionListItem {
        id: item
        title: "City"
        subTitle: selectionDialog.selectedIndex >= 0
                  ? selectionDialog.model.get(selectionDialog.selectedIndex).name
                  : "Please select"

        onClicked: selectionDialog.open()

        SelectionDialog {
            id: selectionDialog
            titleText: "Select one of the values"
            selectedIndex: -1
            model: ListModel {
                ListElement { name: "Helsinki" }
                ListElement { name: "Oulu" }
                ListElement { name: "Rovaniemi" }
                ListElement { name: "Tampere" }
                ListElement { name: "Vaasa" }
            }
        }
}