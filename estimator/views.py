import math
from django.shortcuts import render, redirect
from .models import Project, MeasurementRow

def calculate_view(request):
    if request.method == "POST":
        # 1. Grab basic info from the form
        p_name = request.POST.get('project_name', 'Untitled Project')
        p_pitch = float(request.POST.get('pitch', 0))
        p_notes = request.POST.get('notes', '')

        # 2. Create the Project in the database
        new_project = Project.objects.create(
            name=p_name,
            pitch=p_pitch,
            notes=p_notes
        )

        # 3. Handle the "Infinite" Rows
        lengths = request.POST.getlist('length[]')
        widths = request.POST.getlist('width[]')
        
        flat_sqft = 0
        for l, w in zip(lengths, widths):
            if l and w:
                val_l, val_w = float(l), float(w)
                flat_sqft += (val_l * val_w)
                # Save each individual row to the database linked to this project
                MeasurementRow.objects.create(
                    project=new_project,
                    length=val_l,
                    width=val_w
                )

        # 4. The Math
        multiplier = math.sqrt(1 + (p_pitch / 12)**2)
        actual_sqft = flat_sqft * multiplier
        squares = actual_sqft / 100

        context = {
            'project': new_project,
            'squares': round(squares, 2),
            'sqft': round(actual_sqft, 2),
            'multiplier': round(multiplier, 3),
            'notes': p_notes
        }

        # Inside your calculate_view function:

        # 1. Grab the new inputs
        waste_percent = float(request.POST.get('waste', 10))
        dump_cost = float(request.POST.get('dump', 500))

        # 2. Existing math
        multiplier = math.sqrt(1 + (p_pitch / 12)**2)
        net_squares = (flat_sqft * multiplier) / 100

        # 3. Waste Math
        # Actual squares + waste (e.g., 1.10 for 10%)
        total_squares_to_order = net_squares * (1 + (waste_percent / 100))

        # 4. Add to context so results.html can see it
        context = {
            'net_squares': round(net_squares, 2),
            'order_squares': math.ceil(total_squares_to_order), # Usually rounded up to next full square
            'dump_cost': dump_cost,
            'waste_percent': waste_percent,
        }
        return render(request, 'results.html', context)
    
    return render(request, 'estimator.html')


