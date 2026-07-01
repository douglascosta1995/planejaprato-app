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

        emptyState.classList.remove("hidden");

    }

}


function renderEmptyMeal() {

    return `
        <div class="empty-state-small">
            Nenhuma receita.
        </div>
    `;

}
