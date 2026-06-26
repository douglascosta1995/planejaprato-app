function initIngredientSearch() {
    const searchInput = document.getElementById("ingredient_search");
    const clearButton = document.getElementById("clear-search-btn");
    const resultsContainer = document.getElementById("ingredient-results");

    if (!searchInput || !clearButton || !resultsContainer) return;

    searchInput.addEventListener("input", () => {
        clearButton.style.display =
            searchInput.value.trim() ? "block" : "none";
    });

    searchInput.addEventListener("keydown", (e) => {

        if (e.key === "Enter") {
            e.preventDefault();
            searchIngredient();
        }

    });
}

window.searchIngredient = async function () {
    const value = document.getElementById("ingredient_search")?.value;

    if (!value) return;

    const res = await fetch(`/ingredients/search?q=${value}`);
    const data = await res.json();

    const container = document.getElementById("ingredient-results");
    if (!container) return;

    container.innerHTML = "";

    data.forEach(item => {
        const div = document.createElement("div");
        div.classList.add("ingredient-item");

        div.innerHTML = `
            <span>${item.name}</span>
            <button type="button">adicionar</button>
        `;

        div.querySelector("button").addEventListener("click", () => {
            selectIngredient(item.id, item.name);
        });

        container.appendChild(div);
    });
};

const UNITS = [
    "unidade",
    "g",
    "kg",
    "ml",
    "l",
    "pitada",
    "colher de chá",
    "colher de sopa",
    "xícara"
];

const options = UNITS.map(unit =>
    `<option value="${unit}">${unit}</option>`
).join("");

function selectIngredient(id, name) {
    const container = document.getElementById("selected-ingredients");
    const emptyState = document.getElementById("ingredients-empty-state");

    if (!container) return;

    if (emptyState) {
        emptyState.style.display = "none";
    }

    const div = document.createElement("div");
    div.classList.add("selected-ingredient");

    div.innerHTML = `
        <div class="ingredient-header">
            <h4>${name}</h4>

            <button type="button" class="delete-ingredient-btn">
                🗑️
            </button>
        </div>

        <div class="ingredient-fields">
            <div class="field-group">
                <label>Quantidade</label>

                <input type="hidden" name="ingredient_ids" value="${id}">

                <input
                    type="number"
                    name="quantities"
                    placeholder="0"
                    min="0"
                    step="0.1"
                    required
                >
            </div>

            <div class="field-group">
                <label>Unidade</label>

                <select name="units">
                    ${options}
                </select>
            </div>
        </div>
    `;

    div.querySelector(".delete-ingredient-btn")
        .addEventListener("click", () => div.remove());

    container.appendChild(div);

    const search = document.getElementById("ingredient_search");
    const results = document.getElementById("ingredient-results");

    if (search) search.value = "";
    if (results) results.innerHTML = "";
}

window.clearIngredientSearch = function () {
    const search = document.getElementById("ingredient_search");
    const results = document.getElementById("ingredient-results");
    const clearButton = document.getElementById("clear-search-btn");

    if (search) {
        search.value = "";
        search.focus();
    }

    if (results) results.innerHTML = "";
    if (clearButton) clearButton.style.display = "none";
};

function initClearButton() {
    const searchInput = document.getElementById("ingredient_search");
    const clearButton = document.getElementById("clear-search-btn");

    if (!searchInput || !clearButton) return;

    searchInput.addEventListener("input", () => {
        clearButton.style.display =
            searchInput.value.trim() ? "block" : "none";
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initIngredientSearch();
    initClearButton();
});

async function toggleCategory(recipeId, categoryId, button) {

    const formData = new FormData();
    formData.append("category_id", categoryId);

    const response = await fetch(
        `/recipes/${recipeId}/categories/toggle`,
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    if (data.action === "added") {
        button.classList.add("selected");
    } else {
        button.classList.remove("selected");
    }
}

document.addEventListener("DOMContentLoaded", () => {

    const section =
        document.querySelector(".highlight-section");

    if(section){

        section.scrollIntoView({
            behavior:"smooth",
            block:"center"
        });

    }

});
