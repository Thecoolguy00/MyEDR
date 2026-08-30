const API_URL = "http://localhost:8000/api/v1";


export async function login(
    username,
    password,
) {
    const response = await fetch(
        `${API_URL}/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username,
                password,
            }),
        },
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Login failed",
        );
    }

    return data;
}


export async function logout(token) {
    await fetch(
        `${API_URL}/auth/logout`,
        {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        },
    );
}


export async function getDevices(token) {
    const response = await fetch(
        `${API_URL}/devices`,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        },
    );

    if (!response.ok) {
        throw new Error(
            "Failed to fetch devices",
        );
    }

    return response.json();
}