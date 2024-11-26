// api.js
export async function getApiData() {
    console.log("Fetching API data...");
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({ message: "This is mock API data." });
        }, 10);
    });
}
