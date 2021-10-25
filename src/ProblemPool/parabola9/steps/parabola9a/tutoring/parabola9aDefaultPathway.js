var hints = [{id: "parabola9a-h1", type: "hint", dependencies: [], title: "Know form", text: "The form of the endpoints of the latus rectum is: (h+p,k+2p),(h+p,k-2p).", variabilization: {}}, {id: "parabola9a-h2", type: "hint", dependencies: ["parabola9a-h1"], title: "Plug in", text: "Plug in the values for the endpoints, using the the proper h, k, and p values.", variabilization: {}}, {id: "parabola9a-h3", type: "scaffold", problemType: "MultipleChoice", answerType: "string", hintAnswer: ["(-7,-7) and (-7,9)"], dependencies: ["parabola9a-h2"], title: "Endpoints", text: "What are the endpoints? Use the given formula.", choices: ["(-7,-7) and (-7,9)", "(-7,-7) and (-7,9)"], subHints: [{id: "parabola9a-h3-s1", type: "hint", dependencies: [], title: "Answer", text: "The answer is (-7,7) and (-7,9).", variabilization: {}}], variabilization: {}}, {id: "parabola9a-h4", type: "hint", dependencies: ["parabola9a-h3"], title: "Answer", text: "Therefore, the endpoints are (-7,7) and (-7,9).", variabilization: {}}, ]; export {hints};