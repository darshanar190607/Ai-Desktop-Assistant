from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import random

def browser_ui(request):
    """Render the browser UI template"""
    return render(request, 'web_ui/browser_ui.html')  # Update this line

@csrf_exempt
def browser_navigate(request):
    """Handle browser navigation requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            
            if not url:
                return JsonResponse({'status': 'error', 'message': 'URL is required'}, status=400)
            
            # In a real implementation, this would use a browser automation library
            # like Selenium or Playwright to navigate to the URL
            
            # Simulate a delay for the navigation
            time.sleep(1)
            
            return JsonResponse({
                'status': 'success',
                'message': f'Successfully navigated to {url}',
                'url': url
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def browser_task(request):
    """Handle browser automation task requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_type = data.get('task_type')
            params = data.get('params', {})
            
            if not task_type:
                return JsonResponse({'status': 'error', 'message': 'Task type is required'}, status=400)
            
            # Simulate task execution
            # In a real implementation, this would use browser automation
            time.sleep(2)  # Simulate task execution time
            
            result = {}
            
            if task_type == 'google_search':
                search_query = params.get('search_query')
                if not search_query:
                    return JsonResponse({'status': 'error', 'message': 'Search query is required'}, status=400)
                
                # Simulate Google search
                result = {
                    'status': 'completed',
                    'url': f'https://www.google.com/search?q={search_query}',
                    'result': f'Completed Google search for "{search_query}"'
                }
                
            elif task_type == 'purchase_watch':
                watch_type = params.get('watch_type')
                price_range = params.get('price_range')
                
                if not watch_type or not price_range:
                    return JsonResponse({'status': 'error', 'message': 'Watch type and price range are required'}, status=400)
                
                # Simulate watch purchase process
                watch_types = {
                    'smart_watch': 'Smart Watch',
                    'luxury_watch': 'Luxury Watch',
                    'sports_watch': 'Sports Watch'
                }
                
                price_ranges = {
                    'budget': 'under $100',
                    'mid_range': '$100-$500',
                    'premium': 'over $500'
                }
                
                watch_name = watch_types.get(watch_type, watch_type)
                price_desc = price_ranges.get(price_range, price_range)
                
                # Simulate a purchase process
                steps = [
                    f"Searched for {watch_name} {price_desc}",
                    f"Found {random.randint(5, 20)} results matching criteria",
                    f"Selected top-rated {watch_name}",
                    "Added to cart",
                    "Proceeded to checkout",
                    "Simulated payment process",
                    "Completed purchase"
                ]
                
                result = {
                    'status': 'completed',
                    'url': 'https://www.google.com/search?q=' + '+'.join(f"{watch_name} {price_desc}".split()),
                    'result': '<br>'.join([f"{i+1}. {step}" for i, step in enumerate(steps)])
                }
                
            elif task_type == 'custom_task':
                task_description = params.get('task_description')
                target_website = params.get('target_website')
                
                if not task_description or not target_website:
                    return JsonResponse({'status': 'error', 'message': 'Task description and target website are required'}, status=400)
                
                # Simulate custom task execution
                result = {
                    'status': 'completed',
                    'url': target_website,
                    'result': f'Executed custom task: {task_description}'
                }
            
            else:
                return JsonResponse({'status': 'error', 'message': f'Unknown task type: {task_type}'}, status=400)
            
            return JsonResponse(result)
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)