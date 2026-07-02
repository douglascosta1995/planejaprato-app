let recipePickerContext = {
    mode: null,
    mealType: null,
    day: null,
    mealItemId: null
};

document.addEventListener("DOMContentLoaded", () => {

    const tabs = document.querySelectorAll(".day-tab");

    const panels = document.querySelectorAll(".day-panel");

    tabs.forEach(tab => {

        tab.addEventListener("click", () => {

            tabs.forEach(t => t.classList.remove("active"));

            panels.forEach(p => p.classList.remove("active"));

            tab.classList.add("active");

            document
                .getElementById(`day-${tab.dataset.day}`)
                .classList.add("active");

        });

    });

});

document.addEventListener("DOMContentLoaded", () => {

    const searchInput =
        document.getElementById("recipe-search");

    if (searchInput) {

        searchInput.addEventListener("input", async (e) => {

            console.log("Digitando...", e.target.value);

            const query = e.target.value;

            if (query.length < 2) {
                return;
            }

            await searchRecipes(query);

        });

    }

});

async function searchRecipes(query) {

    const response = await fetch(
        `/recipes/search?q=${query}&meal_type=${currentMealType}`
    );

    const data = await response.json();

    renderRecipeResults(data);

}

function renderRecipeResults(recipes) {

    const container =
        document.getElementById("recipe-search-results");

    container.innerHTML = "";

    if (recipes.length === 0) {

        container.innerHTML = `
            <div class="empty-state-small">
                Nenhuma receita encontrada.
            </div>
        `;

        return;

    }

    recipes.forEach(recipe => {

        const item = document.createElement("div");

        item.classList.add("recipe-result-item");

        item.innerHTML = `
            <span>🍽️ ${recipe.name}</span>
            <span>➜</span>
        `;

        item.onclick = () => {

            selectRecipe(recipe);

        };

        container.appendChild(item);

    });

}

async function selectRecipe(recipe) {

    const formData = new FormData();

    formData.append("recipe_id", recipe.id);

    let url = "";

    const context = recipePickerContext;

    if (context.mode === "add") {

        const mealPlanId =
            document
                .querySelector(".dashboard-container")
                .dataset.mealPlanId;

        formData.append("meal_plan_id", mealPlanId);
        formData.append("day", context.day);
        formData.append("meal_type", context.mealType);

        url = "/meal-plan-items/add";

    }

    if (context.mode === "replace") {

        url = `/meal-plan-items/${context.mealItemId}/replace`;

    }

    const response = await fetch(url, {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.message);
        return;
    }

    if (context.mode === "add") {

        const mealItems = document.getElementById(
            `meal-items-${context.day}-${context.mealType}`
        );

        mealItems.insertAdjacentHTML(
            "beforeend",
            data.html
        );

    }

    if (context.mode === "replace") {

        const oldItem =
            document.getElementById(
                `meal-item-${context.mealItemId}`
            );

        oldItem.outerHTML = data.html;
    }

    closeRecipePicker();

}

async function deleteMealItem(itemId) {

    if (!confirm("Remover esta receita?")) {
        return;
    }

    const response = await fetch(
        `/meal-plan-items/${itemId}/delete`,
        {
            method: "POST"
        }
    );

    const data = await response.json();

    if (!response.ok) {
        alert(data.message);
        return;
    }

    const mealItem = document.getElementById(`meal-item-${itemId}`);

    if (!mealItem) {
        return;
    }

    const mealRecipe = mealItem.closest(".meal-recipe");

    const mealItems = mealRecipe.querySelector(".meal-items");

    const emptyState = mealRecipe.querySelector(".empty-state-small");

    mealItem.remove();

    if (mealItems.children.length === 0) {

        mealItems.innerHTML = `
            <div class="empty-state-small">
                Nenhuma receita.
            </div>
        `;

    }

}


function renderEmptyMeal() {

    return `
        <div class="empty-state-small">
            Nenhuma receita.
        </div>
    `;

}

function openRecipePicker(mode, mealType, day, mealItemId = null){

    recipePickerContext = {
        mode,
        mealType,
        day,
        mealItemId
    };

    currentMealType = mealType;

    document
        .getElementById("recipe-picker-modal")
        .classList.remove("hidden");

    document
        .getElementById("recipe-search")
        .value = "";

    document
        .getElementById("recipe-search-results")
        .innerHTML = "";

}

function closeRecipePicker(){

    document
        .getElementById("recipe-picker-modal")
        .classList.add("hidden");

}
