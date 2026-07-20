import { DashboardContent } from "@/components/dashboard/dashboard-content";
import { Sidebar } from "@/components/dashboard/sidebar";
import { TopNav } from "@/components/dashboard/top-nav";

export default function DashboardPage() { return <div className="flex h-screen overflow-hidden"><Sidebar/><div className="flex min-w-0 flex-1 flex-col"><TopNav/><DashboardContent/></div></div>; }
