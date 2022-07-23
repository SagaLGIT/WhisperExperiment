var hints = [{id: "af4e405log16a-h1", type: "hint", dependencies: [], title: "Convert to Exponential Form", text: "We know that we're trying to solve $$\\log_{a}\\left(121\\right)=2$$. Rewrite this expression first into exponential form.", variabilization: {}}, {id: "af4e405log16a-h2", type: "scaffold", problemType: "MultipleChoice", answerType: "string", hintAnswer: ["$$a^2=121$$"], dependencies: ["af4e405log16a-h1"], title: "Determing the Exponential Form", text: "What is the exponential form of $$\\log_{a}\\left(121\\right)=2$$?", choices: ["$$a^2=121$$", "$${121}^2=a$$", "$${121}^a=2$$", "$$2^a=121$$"], variabilization: {}}, {id: "af4e405log16a-h3", type: "scaffold", problemType: "TextBox", answerType: "arithmetic", hintAnswer: ["11"], dependencies: ["af4e405log16a-h2"], title: "Solve for a", text: "What is the solution for a in the exponential equation $$a^2=121$$? Note that the domain of logarithmic equations is non-negative, so a must be non-negative!", variabilization: {}}, ]; export {hints};