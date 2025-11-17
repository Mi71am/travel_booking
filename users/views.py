from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

# Profile view: GET, update, delete
@login_required
def profile(request):
	user = request.user
	try:
		user_profile = UserProfile.objects.get(user=user)
	except UserProfile.DoesNotExist:
		user_profile = UserProfile.objects.create(user=user)

	if request.method == 'POST':
		if 'delete_account' in request.POST:
			# Delete profile pic file if exists
			if user_profile.profile_pic:
				user_profile.profile_pic.delete(save=False)
			user.delete()
			messages.success(request, 'Your account has been deleted.')
			return redirect('signup')
		elif 'delete_pic' in request.POST:
			if user_profile.profile_pic:
				user_profile.profile_pic.delete(save=False)
				user_profile.profile_pic = None
				user_profile.save()
				messages.success(request, 'Profile picture removed.')
				return redirect('profile')
		elif 'update_profile' in request.POST or True:
			username = request.POST.get('username')
			email = request.POST.get('email')
			phone = request.POST.get('phone')
			account_type = request.POST.get('account_type')
			password = request.POST.get('password')
			confirm = request.POST.get('confirmPassword')
			profile_pic = request.FILES.get('profile_pic')

			# Update user fields
			user.username = username
			user.email = email
			if password:
				if password == confirm:
					user.password = make_password(password)
				else:
					messages.error(request, 'Passwords do not match.')
					return redirect('profile')
			user.save()

			# Update profile fields
			user_profile.phone = phone
			# Save account_type if you add it to UserProfile model
			if hasattr(user_profile, 'account_type'):
				user_profile.account_type = account_type
			if profile_pic:
				if user_profile.profile_pic:
					user_profile.profile_pic.delete(save=False)
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				user_profile.profile_pic = filename
			user_profile.save()
			messages.success(request, 'Profile updated!')
			return redirect('dashboard')

	return render(request, 'users/profile.html', {'user': user, 'user_profile': user_profile})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def user_login(request):
	import logging
	logger = logging.getLogger('django')
	logger.debug('Login view called')
	if request.method == 'POST':
		logger.debug('Login POST received')
		email_or_username = request.POST.get('username')
		password = request.POST.get('password')
		logger.debug(f"Login data: username/email={email_or_username}, password={'*' * len(password) if password else None}")
		user = None
		try:
			user_obj = User.objects.get(email=email_or_username)
			logger.debug(f"Found user by email: {user_obj.username}")
			user = authenticate(request, username=user_obj.username, password=password)
		except User.DoesNotExist:
			logger.debug("No user found by email, trying username directly")
			user = authenticate(request, username=email_or_username, password=password)
		if user is not None:
			logger.info(f"Login successful for user: {user.username}")
			login(request, user)
			return redirect('dashboard')
		else:
			logger.warning(f"Login failed for: {email_or_username}")
			messages.error(request, 'Incorrect email or password')
	else:
		logger.debug('Login GET received')
	return render(request, 'users/login.html')
@login_required
def dashboard(request):
	user_profile = None
	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except UserProfile.DoesNotExist:
		pass
	return render(request, 'users/dashboard.html', {'user': request.user, 'user_profile': user_profile})

def user_logout(request):
	logout(request)
	return redirect('home')

def user_signup(request):
	import logging
	logger = logging.getLogger('django')
	if request.method == 'POST':
		logger.debug('Signup POST received')
		username = request.POST.get('fname')
		email = request.POST.get('email')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirmPassword')
		phone = request.POST.get('pnum')
		account_type = request.POST.get('account_type')
		profile_pic = request.FILES.get('profile_pic')
		logger.debug(f"Signup data: username={username}, email={email}, phone={phone}, account_type={account_type}")
		if password != confirm_password:
			logger.error('Passwords do not match')
			messages.error(request, 'Passwords do not match')
			return render(request, 'users/signup.html')
		if User.objects.filter(username=username).exists():
			logger.error('Username already exists')
			messages.error(request, 'Username already exists')
			return render(request, 'users/signup.html')
		if User.objects.filter(email=email).exists():
			logger.error('Email already exists')
			messages.error(request, 'Email already exists')
			return render(request, 'users/signup.html')
		try:
			user = User.objects.create_user(username=username, email=email, password=password)
			user_profile = UserProfile.objects.create(user=user, phone=phone)
			if profile_pic:
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				user_profile.profile_pic = filename
			user_profile.save()
			logger.info('Account created successfully')
			messages.success(request, 'Account created successfully! Please log in.')
			return redirect('login')
		except Exception as e:
			logger.error(f"Signup error: {e}")
			messages.error(request, f"Signup failed: {e}")
			return render(request, 'users/signup.html')
	logger.debug('Signup GET received')
	return render(request, 'users/signup.html')
