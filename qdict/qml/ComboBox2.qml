mport Qt 4.7
2	
import Qt.labs.components 1.0
3	
4	
Item {
5	
    id:combobox
6	
7	
    width: Math.max(100, labelComponent.item.width + 2*10)
8	
    height: Math.max(32, labelComponent.item.height + 2*4)
9	
10	
    clip:true
11	
    signal clicked
12	
13	
14	
    property int elementsToShow: 5;
15	
    property string currentText;
16	
    property alias model: elements.model;
17	
    property alias currentIndex: elements.currentIndex;
18	
19	
    property alias hover: markerArea.containsMouse
20	
    property bool pressed: false
21	
22	
    property Component background : defaultbackground
23	
    property Component content : defaultlabel
24	
    property Component delegate : defaultDelegate
25	
    property Component highlight : defaultHighlight
26	
27	
    property string text
28	
    property string icon
29	
30	
    property color backgroundColor: "#fff";
31	
    property color foregroundColor: "#333";
32	
33	
    property alias font: fontcontainer.font
34	
35	
    Text {id:fontcontainer; font.pixelSize:14} // Workaround since font is not a declarable type (bug?)
36	
37	
    ListView {
38	
        id: elements;
39	
        anchors.fill: parent;
40	
41	
        clip:true;
42	
        boundsBehavior: "StopAtBounds";
43	
        keyNavigationWraps: true;
44	
45	
        delegate: delegate;
46	
        highlight: highlight;
47	
    }
48	
49	
50	
    // background
51	
    Loader {
52	
        id:backgroundComponent
53	
        anchors.fill:parent
54	
        sourceComponent:background
55	
        opacity: enabled ? 1 : 0.8
56	
    }
57	
58	
    // content
59	
    Loader {
60	
        id:labelComponent
61	
        anchors.centerIn: parent
62	
        sourceComponent:content
63	
    }
64	
65	
    onClicked:{
66	
        list.state == "" ? list.state = "shown" : list.state = "";
67	
        elements.currentIndex = list.lastIndex;
68	
    }
69	
70	
    MouseArea {
71	
        id:markerArea
72	
        enabled: combobox.enabled
73	
        hoverEnabled: true
74	
        anchors.fill: parent
75	
        onPressed: {
76	
            combobox.pressed = true
77	
        }
78	
        onEntered: if(pressed && enabled) combobox.pressed = true  // handles clicks as well
79	
        onExited: {
80	
            combobox.pressed = false
81	
        }
82	
83	
        onReleased: {
84	
            if (combobox.pressed && enabled) { // No click if release outside area
85	
                combobox.pressed  = false
86	
                combobox.clicked()
87	
            }
88	
        }
89	
    }
90	
91	
    Component {
92	
        id:defaultbackground
93	
        Item {
94	
95	
            Rectangle{
96	
                color:backgroundColor
97	
                radius: 5
98	
                x:1
99	
                y:1
100	
                width:parent.width-2
101	
                height:parent.height-2
102	
            }
103	
104	
            BorderImage {
105	
                anchors.fill:parent
106	
                id: backgroundimage
107	
                smooth:true
108	
                source: pressed ? "images/button_pressed.png" : "images/button_normal.png"
109	
                width: 80; height: 24
110	
                border.left: 3; border.top: 3
111	
                border.right: 3; border.bottom: 3
112	
113	
                Image{
114	
                    anchors.top:parent.top
115	
                    anchors.right: parent.right
116	
                    anchors.topMargin: 7
117	
                    anchors.rightMargin: 7
118	
                    opacity: enabled ? 1 : 0.3
119	
                    source:"images/spinbox_up.png"
120	
                }
121	
                Image{
122	
                    anchors.bottom:parent.bottom;
123	
                    anchors.right: parent.right
124	
                    anchors.bottomMargin: 7
125	
                    anchors.rightMargin: 7
126	
                    opacity: enabled ? 1 : 0.3
127	
                    source:"images/spinbox_down.png"
128	
                }
129	
            }
130	
        }
131	
    }
132	
133	
    Component {
134	
        id:defaultlabel
135	
        Item {
136	
            width:layout.width
137	
            height:layout.height
138	
            anchors.margins:4
139	
            Row {
140	
                spacing:6
141	
                anchors.centerIn:parent
142	
                id:layout
143	
                Image { source:combobox.icon; anchors.verticalCenter:parent.verticalCenter}
144	
                Text {
145	
                    id:label
146	
                    font:combobox.font
147	
                    color:combobox.foregroundColor;
148	
                    anchors.verticalCenter: parent.verticalCenter ;
149	
                    text:combobox.text
150	
                    opacity:parent.enabled ? 1 : 0.5
151	
                }
152	
            }
153	
        }
154	
    }
155	
156	
    Component {
157	
        id: defaultDelegate
158	
        Item {
159	
            id: wrapper
160	
            width: background.width;
161	
            height: background.height;
162	
163	
            Row {
164	
                x: 5;
165	
                y: 5;
166	
                spacing: 5;
167	
                Text {
168	
                    font.pixelSize: mx.fontSize
169	
                    color: mx.fontColor
170	
                    text: content;
171	
                }
172	
                Image {
173	
                    source: icon;
174	
                    anchors.verticalCenter: parent.verticalCenter;
175	
                    height: wrapper.height - 10;
176	
                }
177	
            }
178	
179	
            function selectItem(index) {
180	
                combobox.current = elements.model.get(index).content;
181	
                list.lastIndex = index;
182	
                list.state = "";
183	
            }
184	
185	
            MouseArea {
186	
                anchors.fill: parent;
187	
                hoverEnabled: true;
188	
189	
                onEntered: {
190	
                    elements.currentIndex = index;
191	
                }
192	
                onClicked: selectItem(index);
193	
            }
194	
195	
            Keys.onPressed: {
196	
                if (event.key == Qt.Key_Enter || event.key == Qt.Key_Return) {
197	
                    selectItem(index);
198	
                } else if (event.key == Qt.Key_Escape) {
199	
                    list.state = "";
200	
                }
201	
            }
202	
        }
203	
    }
204	
205	
    Component {
206	
        id: defaultHighlight
207	
        Rectangle {
208	
            color: "#cccccc";
209	
            x:1
210	
            width:parent.width-2
211	
        }
212	
    }
213	
214	
    Item {
215	
        id: list;
216	
        property int lastIndex;
217	
218	
        opacity: 0;
219	
        height: Math.min(background.height * elements.count,
220	
                         background.height * combobox.elementsToShow);
221	
222	
        anchors.top: background.bottom;
223	
        anchors.left: background.left;
224	
        anchors.right: background.right;
225	
226	
        Component {
227	
            id: delegate
228	
            Item {
229	
                id: wrapper
230	
                width: background.width;
231	
                height: background.height;
232	
233	
                Row {
234	
                    x: 5;
235	
                    y: 5;
236	
                    spacing: 5;
237	
                    Text {
238	
                        font.pixelSize: mx.fontSize
239	
                        color: mx.fontColor
240	
                        text: content;
241	
                    }
242	
                    Image {
243	
                        source: icon;
244	
                        anchors.verticalCenter: parent.verticalCenter;
245	
                        height: wrapper.height - 10;
246	
                    }
247	
                }
248	
249	
                function selectItem(index) {
250	
                    combobox.current = elements.model.get(index).content;
251	
                    list.lastIndex = index;
252	
                    list.state = "";
253	
                }
254	
255	
                MouseArea {
256	
                    anchors.fill: parent;
257	
                    hoverEnabled: true;
258	
259	
                    onEntered: {
260	
                        elements.currentIndex = index;
261	
                    }
262	
                    onClicked: selectItem(index);
263	
                }
264	
265	
                Keys.onPressed: {
266	
                    if (event.key == Qt.Key_Enter || event.key == Qt.Key_Return) {
267	
                        selectItem(index);
268	
                    } else if (event.key == Qt.Key_Escape) {
269	
                        list.state = "";
270	
                    }
271	
                }
272	
            }
273	
        }
274	
    }
275	
}