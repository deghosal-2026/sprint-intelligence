export default function Admin() {
  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Admin</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="font-semibold mb-2">Poller Controls</h2>
          <div className="flex gap-2">
            <button className="bg-blue-500 text-white px-3 py-1 rounded text-sm">
              Fetch Data
            </button>
            <button className="bg-green-500 text-white px-3 py-1 rounded text-sm">
              Compute Metrics
            </button>
            <button className="bg-purple-500 text-white px-3 py-1 rounded text-sm">
              Full Poll
            </button>
          </div>
          <p className="text-xs text-gray-400 mt-2">
            Status: Idle
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="font-semibold mb-2">System Status</h2>
          <div className="space-y-1 text-sm">
            <p>DB: <span className="text-yellow-500">Checking...</span></p>
            <p>Ollama: <span className="text-yellow-500">Checking...</span></p>
            <p>GitHub API: <span className="text-yellow-500">-- remaining</span></p>
          </div>
        </div>
      </div>
    </div>
  );
}
