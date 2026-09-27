import json
import os
import argparse
from rich.console import Console
from rich.table import Table
from .physics import solve_radius, nm_to_ev

def load_database():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'materials.json')
    with open(db_path, 'r') as f:
        return json.load(f)

def run_cli():
    parser = argparse.ArgumentParser(description="Spectral Sieve: Nanomaterial Bandgap Tuner")
    parser.add_argument("wavelength", type=float, help="Target emission wavelength in nm")
    parser.add_argument("--non-toxic", action="store_true", help="Filter out toxic materials")
    args = parser.parse_args()

    console = Console()
    target_nm = args.wavelength
    target_ev = nm_to_ev(target_nm)

    console.print(f"\n[bold blue]Spectral Sieve[/bold blue]")
    console.print(f"Target Emission: [bold]{target_nm} nm[/bold] ({target_ev:.3f} eV)\n")

    db = load_database()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Material", style="cyan")
    table.add_column("Required Radius (nm)", justify="right")
    table.add_column("Required Diameter (nm)", justify="right")
    table.add_column("Toxicity")

    results_found = False

    for name, props in db.items():
        if args.non_toxic and props["toxic"]:
            continue
            
        r_nm = solve_radius(target_nm, props)
        
        if r_nm is None:
            table.add_row(name, "[dim]Unreachable[/dim]", "[dim]Unreachable[/dim]", "Toxic" if props["toxic"] else "Safe")
        else:
            results_found = True
            toxicity = "[red]Toxic[/red]" if props["toxic"] else "[green]Safe[/green]"
            table.add_row(name, f"{r_nm:.2f}", f"{r_nm*2:.2f}", toxicity)

    console.print(table)
    
    if not results_found:
        console.print("\n[yellow]Warning:[/yellow] No valid materials found for this wavelength within feasible synthetic size constraints (1-40 nm diameter).")
    console.print()