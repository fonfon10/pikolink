class OwnersController < InheritedResources::Base

  before_action :authenticate_user!


def index
  @q = Owner.where(user_id: current_user.id).ransack(params[:q])
  @owners = @q.result.includes(:company).page(params[:page])


end


def new
  @owner = Owner.new
  @companies = Company.where("user_id = ?", current_user.id).order('name ASC').map { |i| [i.name, i.id]}
end

def create
  @owner = Owner.new(owner_params)

  @owner.company_id = params[:company_id]
  @owner.user_id = current_user.id

  if @owner.save
    redirect_to root_path
  else
    render 'new'
  end
  
end



def edit
  @owner = Owner.find(params[:id])    
  @companies = Company.all.order('name ASC').map { |i| [i.name, i.id]}
end


def destroy

  @owner = Owner.find(params[:id])
  @owner.destroy
  redirect_to owners_url, notice: "Engineer was successfully destroyed"

end



  private

    def owner_params
      params.require(:owner).permit(:firstname, :lastname, :email, :company_id, :user_id)
    end
end
