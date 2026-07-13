document.addEventListener("DOMContentLoaded", () => {

    document
        .querySelectorAll(".shopping-quantity-input, .shopping-unit-input, .shopping-comment-input")
        .forEach(field => {

            field.addEventListener("blur", () => {

                saveShoppingItem(field.dataset.itemId);

            });

        });

});


async function saveShoppingItem(itemId) {

    const quantityInput = document.querySelector(
        `.shopping-quantity-input[data-item-id="${itemId}"]`
    );

    const unitInput = document.querySelector(
        `.shopping-unit-input[data-item-id="${itemId}"]`
    );

    const noteInput = document.querySelector(
        `.shopping-comment-input[data-item-id="${itemId}"]`
    );

    const formData = new FormData();

    formData.append("quantity", quantityInput.value);
    formData.append("unit", unitInput.value);
    formData.append("note", noteInput.value);

    const response = await fetch(
        `/shopping-list-items/${itemId}/update`,
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    console.log(data);
}

document
    .querySelectorAll(".delete-ingredient-btn")
    .forEach(button => {

        button.addEventListener("click", () => {

            deleteShoppingItem(button.dataset.itemId);

        });

    });


async function deleteShoppingItem(itemId) {

    if (!confirm("Remover este produto da lista?")) {
        return;
    }

    const response = await fetch(
        `/shopping-list-items/${itemId}/delete`,
        {
            method: "POST"
        }
    );

    const data = await response.json();

    if (data.success) {

        document
            .querySelector(`.shopping-item[data-item-id="${itemId}"]`)
            .remove();

    }

}


document.addEventListener("DOMContentLoaded", () => {

    const button = document.getElementById("show-manual-input-btn");

    if (button) {
        button.addEventListener("click", showManualItemInput);
    }

});

function showManualItemInput() {

    const button = document.getElementById("show-manual-input-btn");
    const container = document.getElementById("manual-item-input-container");

    button.style.display = "none";

    container.innerHTML = `
        <input
            id="manual-item-input"
            type="text"
            class="shopping-comment-input"
            placeholder="Ex.: 2 rolos de papel higiênico"
        >
    `;

    const input = document.getElementById("manual-item-input");

    input.focus();

    input.addEventListener("blur", async () => {

    if (input.value.trim() === "") {

        container.innerHTML = "";
        button.style.display = "inline-block";
        return;

    }

    const shoppingList = document.querySelector(".shopping-list");

    const shoppingListId =
        shoppingList.dataset.shoppingListId;

    const formData = new FormData();

    formData.append(
        "manual_name",
        input.value
    );
    console.log(shoppingListId);
    console.log(input.value);

    const response = await fetch(
        `/shopping-lists/${shoppingListId}/manual-item`,
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    if (data.success) {

        shoppingList.insertAdjacentHTML(
            "beforeend",
            data.html
        );

    }

    container.innerHTML = "";

    button.style.display = "inline-block";

});

}
