import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import Dashboard from "../pages/Dashboard.jsx";

vi.mock("recharts", () => ({
  ResponsiveContainer: ({ children }) => <div>{children}</div>,
  BarChart: ({ children }) => <div>{children}</div>,
  Bar: () => <div />,
  XAxis: () => <div />,
  YAxis: () => <div />,
  CartesianGrid: () => <div />,
  Tooltip: () => <div />,
  Legend: () => <div />,
  LineChart: ({ children }) => <div>{children}</div>,
  Line: () => <div />,
}));

beforeEach(() => {
  const mockSprints = [{ id: 1, name: "team1-2026.24.25", start_date: "2026-06-15", end_date: "2026-06-28" }];
  const mockMetrics = { velocity_ratio: 0.8, completed_points: 40, planned_points: 50 };
  const mockEngineers = [{ engineer: "team1-engineer1", completed_points: 10 }];
  global.fetch = vi.fn((url) => {
    if (typeof url === "string" && url.endsWith("/sprints")) {
      return Promise.resolve({ json: () => Promise.resolve(mockSprints) });
    }
    if (typeof url === "string" && url.includes("/engineers")) {
      return Promise.resolve({ json: () => Promise.resolve(mockEngineers) });
    }
    return Promise.resolve({ json: () => Promise.resolve(mockMetrics) });
  });
  sessionStorage.clear();
});

function setPersona(persona) {
  sessionStorage.setItem("sprintsense_persona", persona);
}

describe("T3.1: Junior personal cards only", () => {
  it("shows My Cycle Time in junior view", () => {
    setPersona("junior");
    render(<Dashboard />);
    expect(screen.getByText("My Cycle Time")).toBeInTheDocument();
  });

  it("shows My Points in junior view", () => {
    setPersona("junior");
    render(<Dashboard />);
    expect(screen.getByText("My Points")).toBeInTheDocument();
  });

  it("shows My WIP in junior view", () => {
    setPersona("junior");
    render(<Dashboard />);
    expect(screen.getByText("My WIP")).toBeInTheDocument();
  });

  it("shows Coach Tip in junior view", () => {
    setPersona("junior");
    render(<Dashboard />);
    expect(screen.getByText("Coach Tip")).toBeInTheDocument();
  });

  it("does not show team table in junior view", () => {
    setPersona("junior");
    render(<Dashboard />);
    expect(screen.queryByText("Engineers")).not.toBeInTheDocument();
  });
});

describe("T3.2: Senior team aggregate", () => {
  it("shows My Velocity in senior view", () => {
    setPersona("senior");
    render(<Dashboard />);
    expect(screen.getByText("My Velocity")).toBeInTheDocument();
  });

  it("shows Reviews Done in senior view", () => {
    setPersona("senior");
    render(<Dashboard />);
    expect(screen.getByText("Reviews Done")).toBeInTheDocument();
  });

  it("shows Team Velocity in senior view", () => {
    setPersona("senior");
    render(<Dashboard />);
    expect(screen.getByText("Team Velocity")).toBeInTheDocument();
  });
});

describe("T3.3: Staff cycle time comparison", () => {
  it("shows Blocked Issues in staff view", () => {
    setPersona("staff");
    render(<Dashboard />);
    expect(screen.getByText("Blocked Issues")).toBeInTheDocument();
  });

  it("shows Unblocking Requests in staff view", () => {
    setPersona("staff");
    render(<Dashboard />);
    expect(screen.getByText("Unblocking Requests")).toBeInTheDocument();
  });
});

describe("T3.4: Persona toggle switches cards", () => {
  it("shows SDM-specific cards when persona is sdm", () => {
    setPersona("sdm");
    render(<Dashboard />);
    expect(screen.getByText("Capacity")).toBeInTheDocument();
    expect(screen.getByText("Bug Rate")).toBeInTheDocument();
  });

  it("does not show Velocity card in junior view", () => {
    setPersona("junior");
    render(<Dashboard />);
    expect(screen.queryByText("Velocity")).not.toBeInTheDocument();
  });

  it("does not show DORA Pulse in senior view", () => {
    setPersona("senior");
    render(<Dashboard />);
    expect(screen.queryByText("DORA Pulse")).not.toBeInTheDocument();
  });
});
