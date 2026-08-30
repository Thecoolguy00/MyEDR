import {
    useEffect,
    useState,
} from "react";

import {
    getDevices,
    logout,
} from "../api";


export default function Dashboard({
    token,
    onLogout,
}) {
    const [devices, setDevices] =
        useState([]);

    const [error, setError] =
        useState("");

    const [loading, setLoading] =
        useState(true);


    useEffect(() => {

        async function loadDevices() {
            try {
                const data =
                    await getDevices(token);

                setDevices(data);

            } catch (error) {
                setError(error.message);

            } finally {
                setLoading(false);
            }
        }

        loadDevices();

    }, [token]);


    async function handleLogout() {
        try {
            await logout(token);
        } finally {
            localStorage.removeItem(
                "access_token",
            );

            onLogout();
        }
    }


    return (
        <div className="dashboard">

            <header>
                <h1>MyEDR</h1>

                <button
                    onClick={handleLogout}
                >
                    Logout
                </button>
            </header>

            <main>

                <h2>Devices</h2>

                {loading && (
                    <p>Loading devices...</p>
                )}

                {error && (
                    <p className="error">
                        {error}
                    </p>
                )}

                {!loading && !error && (
                    <table>

                        <thead>
                            <tr>
                                <th>Hostname</th>
                                <th>OS</th>
                                <th>CPU</th>
                                <th>RAM</th>
                            </tr>
                        </thead>

                        <tbody>

                            {devices.map(
                                (device) => (
                                    <tr
                                        key={
                                            device.id
                                        }
                                    >
                                        <td>
                                            {
                                                device.hostname
                                            }
                                        </td>

                                        <td>
                                            {
                                                device.os_name
                                            }
                                        </td>

                                        <td>
                                            {
                                                device.cpu
                                            }
                                        </td>

                                        <td>
                                            {
                                                (
                                                    device.ram_bytes /
                                                    1024 /
                                                    1024 /
                                                    1024
                                                ).toFixed(2)
                                            } GB
                                        </td>

                                    </tr>
                                )
                            )}

                        </tbody>

                    </table>
                )}

            </main>

        </div>
    );
}