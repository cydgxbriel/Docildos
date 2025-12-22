import { Badge } from "@/components/ui/badge";
import { Clock, Users, DollarSign } from "lucide-react";

interface Ingredient {
  name: string;
  quantity: string;
  unit: string;
}

interface Recipe {
  id: string;
  name: string;
  description?: string;
  prepTime: number;
  yield: string;
  estimatedCost: number;
  ingredients: Ingredient[];
}

interface RecipeCardProps {
  recipe: Recipe;
}

export function RecipeCard({ recipe }: RecipeCardProps) {
  return (
    <div className="bg-card rounded-xl p-4 shadow-card border border-border/50 animate-fade-in">
      <div className="mb-3">
        <h4 className="font-display font-semibold text-lg text-foreground">
          {recipe.name}
        </h4>
        {recipe.description && (
          <p className="text-sm text-muted-foreground mt-1">
            {recipe.description}
          </p>
        )}
      </div>

      <div className="flex flex-wrap gap-3 mb-4">
        <Badge variant="secondary" className="gap-1.5 font-normal">
          <Clock className="w-3.5 h-3.5" />
          {recipe.prepTime} min
        </Badge>
        <Badge variant="secondary" className="gap-1.5 font-normal">
          <Users className="w-3.5 h-3.5" />
          Rende {recipe.yield}
        </Badge>
        <Badge variant="secondary" className="gap-1.5 font-normal">
          <DollarSign className="w-3.5 h-3.5" />
          R$ {recipe.estimatedCost.toFixed(2)}
        </Badge>
      </div>

      <div className="border-t border-border pt-3">
        <h5 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
          Ingredientes
        </h5>
        <div className="grid grid-cols-2 gap-x-4 gap-y-1.5">
          {recipe.ingredients.map((ingredient, index) => (
            <div
              key={index}
              className="flex items-center justify-between text-sm"
            >
              <span className="text-foreground">{ingredient.name}</span>
              <span className="text-muted-foreground">
                {ingredient.quantity}
                {ingredient.unit}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
