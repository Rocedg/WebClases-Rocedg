// Normalize only legacy text in memory; canonical source never uses dollars.
function normalizeLegacyExerciseMath(root) {
    root.querySelectorAll('[data-legacy-math]').forEach(function (element) {
        const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
        const nodes = [];
        while (walker.nextNode()) nodes.push(walker.currentNode);
        nodes.forEach(function (node) {
            if (node.parentElement.closest('mjx-container, script, style, textarea, code, pre')) return;
            node.nodeValue = node.nodeValue
                .replace(/\$\$([\s\S]+?)\$\$/g, '\\[$1\\]')
                .replace(/\$([^$\n]+?)\$/g, '\\($1\\)');
        });
    });
}

window.MathJax = {
    loader: {load: ['ui/safe']},
    tex: {
        inlineMath: [['\\(', '\\)']],
        displayMath: [['\\[', '\\]']]
    },
    options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
        safeOptions: {allow: {URLs: 'none', classes: 'none', cssIDs: 'none', styles: 'none'}}
    },
    startup: {
        ready: function () {
            normalizeLegacyExerciseMath(document);
            MathJax.startup.defaultReady();
        }
    }
};

// Invoke after dynamic insertion; serialize consecutive updates.
let exerciseTypesetting = Promise.resolve();
window.typesetExercise = function (root) {
    exerciseTypesetting = exerciseTypesetting.then(async function () {
        if (!window.MathJax.startup) return;
        await MathJax.startup.promise;
        normalizeLegacyExerciseMath(root);
        await MathJax.typesetPromise([root]);
    }).catch(function (error) { console.error('No se pudieron renderizar las fórmulas.', error); });
    return exerciseTypesetting;
};
document.addEventListener('exercise:rendered', function (event) {
    window.typesetExercise(event.target);
});
document.addEventListener('toggle', function (event) {
    if (event.target.matches('details.exercise-solution[open]')) window.typesetExercise(event.target);
}, true);
