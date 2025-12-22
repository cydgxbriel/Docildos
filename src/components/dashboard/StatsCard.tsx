import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface StatsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: {
    value: number;
    positive: boolean;
  };
  variant?: "default" | "primary" | "warning" | "success";
}

const variantStyles = {
  default: "bg-card",
  primary: "bg-primary/10 border-primary/20",
  warning: "bg-warning/10 border-warning/20",
  success: "bg-success/10 border-success/20",
};

const iconStyles = {
  default: "bg-secondary text-secondary-foreground",
  primary: "bg-primary/20 text-primary",
  warning: "bg-warning/20 text-warning",
  success: "bg-success/20 text-success",
};

export function StatsCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  variant = "default",
}: StatsCardProps) {
  return (
    <div
      className={cn(
        "rounded-xl p-4 border border-border/50 shadow-card transition-all duration-200 hover:shadow-soft",
        variantStyles[variant]
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
            {title}
          </p>
          <p className="text-2xl font-display font-bold text-foreground mt-1">
            {value}
          </p>
          {subtitle && (
            <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>
          )}
          {trend && (
            <p
              className={cn(
                "text-xs font-medium mt-1",
                trend.positive ? "text-success" : "text-destructive"
              )}
            >
              {trend.positive ? "+" : ""}
              {trend.value}% vs. ontem
            </p>
          )}
        </div>
        <div
          className={cn(
            "w-10 h-10 rounded-lg flex items-center justify-center",
            iconStyles[variant]
          )}
        >
          <Icon className="w-5 h-5" />
        </div>
      </div>
    </div>
  );
}
