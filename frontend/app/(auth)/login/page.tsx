import Link from "next/link";
import { AuthForm } from "@/components/auth/auth-form";

export default function LoginPage() { return <><Link href="/" className="mb-12 block text-xl font-semibold lg:hidden">FORGE<span className="text-emerald-400">AI</span></Link><p className="text-sm font-medium uppercase tracking-[0.2em] text-emerald-400">Welcome back</p><h1 className="mt-3 text-3xl font-semibold">Sign in to your workspace</h1><p className="mt-3 text-slate-400">Track emerging problems and design what comes next.</p><div className="mt-8"><AuthForm mode="login" /></div></>; }
