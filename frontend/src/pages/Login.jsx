import { useState } from "react";

import { login } from "../api";


export default function Login({
    onLogin,
}) {
    const [username, setUsername] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [error, setError] =
        useState("");

    const [loading, setLoading] =
        useState(false);


    async function handleSubmit(event) {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            const data = await login(
                username,
                password,
            );

            localStorage.setItem(
                "access_token",
                data.access_token,
            );

            onLogin(data.access_token);

        } catch (error) {
            setError(error.message);

        } finally {
            setLoading(false);
        }
    }


    return (
        <div className="login-page">

            <form
                className="login-card"
                onSubmit={handleSubmit}
            >
                <h1>MyEDR</h1>

                <p>
                    Admin Dashboard
                </p>

                {error && (
                    <div className="error">
                        {error}
                    </div>
                )}

                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(event) =>
                        setUsername(
                            event.target.value,
                        )
                    }
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(event) =>
                        setPassword(
                            event.target.value,
                        )
                    }
                />

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading
                        ? "Logging in..."
                        : "Login"}
                </button>

            </form>

        </div>
    );
}