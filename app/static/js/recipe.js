function initIngredientSearch() {
    const searchInput = document.getElementById("ingredient_search");
    const clearButton = document.getElementById("clear-search-btn");
    const resultsContainer = document.getElementById("ingredient-results");

    if (!searchInput || !clearButton || !resultsContainer) return;

    searchInput.addEventListener("input", () => {
        clearButton.style.display =
            searchInput.value.trim() ? "block" : "none";
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
                    <option value="g">g</option>
                    <option value="kg">kg</option>
                    <option value="ml">ml</option>
                    <option value="l">l</option>
                    <option value="un">unidade</option>
                    <option value="colher">colher</option>
                    <option value="xícara">xícara</option>
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
