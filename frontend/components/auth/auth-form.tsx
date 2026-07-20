"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const isLogin = mode === "login";
  return (
    <form className="space-y-5" onSubmit={(event) => event.preventDefault()}>
      {!isLogin && <Field label="Full name" placeholder="Ada Lovelace" />}
      <Field label="Work email" placeholder="you@company.com" type="email" />
      <Field label="Password" placeholder="••••••••" type="password" />
      <Button className="w-full" size="lg">{isLogin ? "Sign in to ForgeAI" : "Create workspace"}</Button>
      <p className="text-center text-sm text-slate-400">{isLogin ? "New to ForgeAI?" : "Already have an account?"} <Link className="font-medium text-emerald-400 hover:text-emerald-300" href={isLogin ? "/register" : "/login"}>{isLogin ? "Create an account" : "Sign in"}</Link></p>
    </form>
  );
}

function Field({ label, ...props }: { label: string } & React.InputHTMLAttributes<HTMLInputElement>) {
  return <label className="block space-y-2 text-sm font-medium text-slate-200"><span>{label}</span><input className="h-11 w-full rounded-lg border border-slate-700 bg-slate-950/60 px-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-400/20" required {...props} /></label>;
}
